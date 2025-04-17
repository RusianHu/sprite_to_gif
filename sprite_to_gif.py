import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD # 用于拖拽
#注意安装必须的库
#pip install Pillow tkinterdnd2
#启动
#python sprite_to_gif.py

class SpriteSheetConverter(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("序列贴图转 GIF")
        self.geometry("550x800") # 调整窗口大小以容纳预览和控件
        self.resizable(False, False) # 禁止调整窗口大小

        # --- 状态变量 ---
        self.input_filepath = None
        self.gif_frames_pil = [] # 存储 PIL Image 对象
        self.gif_frames_tk = []  # 存储 Tkinter PhotoImage 对象 (用于预览)
        self.preview_job = None
        self.current_preview_frame_index = 0
        self.animation_delay = 100 # GIF 帧之间的延迟 (毫秒)
        self.sprite_format = tk.StringVar(value="4x4") # 默认为4x4格式

        # --- 界面布局 ---
        self.mainframe = ttk.Frame(self, padding="10 10 10 10")
        self.mainframe.pack(fill=tk.BOTH, expand=True)

        # --- 格式选择区 ---
        format_frame = ttk.LabelFrame(self.mainframe, text="选择序列贴图格式", padding="10")
        format_frame.pack(fill=tk.X, pady=5)

        format_4x4 = ttk.Radiobutton(format_frame, text="4x4 格式 (16帧)", variable=self.sprite_format, value="4x4")
        format_4x4.pack(side=tk.LEFT, padx=20, pady=5)

        format_3x4 = ttk.Radiobutton(format_frame, text="3x4 格式 (12帧)", variable=self.sprite_format, value="3x4")
        format_3x4.pack(side=tk.LEFT, padx=20, pady=5)

        # --- 文件输入区 ---
        input_frame = ttk.LabelFrame(self.mainframe, text="输入 PNG 文件", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        input_frame.drop_target_register(DND_FILES)
        input_frame.dnd_bind('<<Drop>>', self.handle_drop)

        self.drop_label = ttk.Label(input_frame, text="将序列贴图 PNG 拖拽到此处", relief="solid", padding=20, anchor=tk.CENTER)
        self.drop_label.pack(fill=tk.X, pady=5)

        browse_button = ttk.Button(input_frame, text="或 浏览...", command=self.select_file)
        browse_button.pack(pady=5)

        self.filepath_label = ttk.Label(input_frame, text="未选择文件")
        self.filepath_label.pack(fill=tk.X, pady=5)

        # --- 预览区 ---
        preview_frame = ttk.LabelFrame(self.mainframe, text="GIF 预览", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)  # 增加上下间距

        # 使用 Canvas 来更好地控制预览图像的大小和位置
        self.preview_canvas = tk.Canvas(preview_frame, bg="lightgrey", width=256, height=256) # 假设帧大小不超过 256x256
        self.preview_canvas.pack(pady=5)  # 减少预览区域的上下间距
        self.preview_label_text = self.preview_canvas.create_text(128, 128, text="预览区域", fill="grey")

        # --- 控制区 ---
        control_frame = ttk.Frame(self.mainframe, padding="5")
        control_frame.pack(fill=tk.X, pady=5)  # 减少控制区的上下间距和内边距

        self.convert_button = ttk.Button(control_frame, text="转换为 GIF", command=self.convert_to_gif, state=tk.DISABLED)
        self.convert_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(control_frame, text="保存 GIF", command=self.save_gif, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # --- 状态栏 ---
        self.status_label = ttk.Label(self.mainframe, text="请选择序列贴图格式和 PNG 文件", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))  # 增加上方的间距

        # --- 样式 ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat")
        style.configure("TLabel", padding=5)
        style.configure("TLabelframe.Label", padding=5)


    def update_status(self, message):
        """更新状态栏信息"""
        self.status_label.config(text=message)
        self.update_idletasks() # 强制更新界面

    def select_file(self):
        """弹出文件选择对话框"""
        format_text = "4x4" if self.sprite_format.get() == "4x4" else "3x4"
        filepath = filedialog.askopenfilename(
            title=f"选择 {format_text} PNG 序列图",
            filetypes=[("PNG 文件", "*.png")]
        )
        if filepath:
            self.process_selected_file(filepath)

    def handle_drop(self, event):
        """处理拖拽进来的文件"""
        filepath = event.data
        # tkinterdnd2 可能返回带花括号的路径，需要清理
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]

        if filepath and filepath.lower().endswith(".png"):
            # 检查是否是单个文件（虽然拖拽通常是单个）
            if os.path.isfile(filepath):
                 self.process_selected_file(filepath)
            else:
                 self.update_status("错误：请拖拽单个 PNG 文件")
                 messagebox.showerror("错误", "请拖拽单个 PNG 文件。")
        else:
            self.update_status("错误：请拖拽有效的 PNG 文件")
            messagebox.showerror("错误", "请拖拽有效的 PNG 文件。")

    def process_selected_file(self, filepath):
        """处理选定或拖拽的文件路径"""
        self.input_filepath = filepath
        self.filepath_label.config(text=os.path.basename(filepath))
        self.update_status(f"已选择文件: {os.path.basename(filepath)}")
        self.convert_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.clear_preview()
        self.gif_frames_pil = []
        self.gif_frames_tk = []

    def clear_preview(self):
        """清除预览区域"""
        if self.preview_job:
            self.after_cancel(self.preview_job)
            self.preview_job = None
        self.preview_canvas.delete("all") # 清除 Canvas 上的所有内容
        self.preview_label_text = self.preview_canvas.create_text(128, 128, text="预览区域", fill="grey")
        self.gif_frames_tk = [] # 清空 tk 图片缓存

    def convert_to_gif(self):
        """执行转换操作"""
        if not self.input_filepath:
            messagebox.showerror("错误", "请先选择一个 PNG 文件。")
            return

        self.update_status("正在转换...")
        self.convert_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.clear_preview()
        self.gif_frames_pil = []
        self.gif_frames_tk = []

        try:
            img = Image.open(self.input_filepath)
            img_width, img_height = img.size

            # 检查是否为 RGBA 模式，如果不是，转换为 RGBA 以支持透明度
            if img.mode != 'RGBA':
                 img = img.convert('RGBA')

            # 根据选择的格式确定行列数
            format_type = self.sprite_format.get()
            if format_type == "4x4":
                rows, cols = 4, 4
                # 直接计算帧大小，不再检查是否能整除
                frame_width = img_width // 4
                frame_height = img_height // 4
            else:  # 3x4格式
                rows, cols = 4, 3
                # 直接计算帧大小，不再检查是否能整除
                frame_width = img_width // 3
                frame_height = img_height // 4

            if frame_width <= 0 or frame_height <= 0:
                 raise ValueError("计算出的帧尺寸无效。")

            for row in range(rows):
                for col in range(cols):
                    left = col * frame_width
                    top = row * frame_height
                    right = left + frame_width
                    bottom = top + frame_height
                    frame = img.crop((left, top, right, bottom))
                    self.gif_frames_pil.append(frame)
                    # 为预览准备 Tkinter PhotoImage
                    tk_image = ImageTk.PhotoImage(frame)
                    self.gif_frames_tk.append(tk_image) # 存储引用防止被回收

            if not self.gif_frames_pil:
                 raise ValueError("未能成功提取任何帧。")

            self.update_status("转换完成！可以预览和保存。")
            self.save_button.config(state=tk.NORMAL)
            # 调整 Canvas 大小以适应第一帧
            self.preview_canvas.config(width=frame_width, height=frame_height)
            self.preview_canvas.delete(self.preview_label_text) # 删除 "预览区域" 文本
            self.start_preview()

        except FileNotFoundError:
            self.update_status(f"错误：文件未找到 - {self.input_filepath}")
            messagebox.showerror("错误", f"文件未找到:\n{self.input_filepath}")
        except Exception as e:
            self.update_status(f"转换错误: {e}")
            messagebox.showerror("转换错误", f"处理图像时发生错误:\n{e}")
            self.clear_preview() # 出错时也清理预览

        finally:
            # 无论成功失败，转换按钮都恢复可用，除非是文件找不到等硬性错误
            if self.input_filepath and os.path.exists(self.input_filepath):
                 self.convert_button.config(state=tk.NORMAL)
            else:
                 self.convert_button.config(state=tk.DISABLED) # 如果文件没了就禁用


    def start_preview(self):
        """开始播放 GIF 预览"""
        if not self.gif_frames_tk:
            return
        if self.preview_job:
            self.after_cancel(self.preview_job)

        self.current_preview_frame_index = 0
        self.animate_preview()

    def animate_preview(self):
        """更新预览画布上的图像以显示动画的下一帧"""
        if not self.gif_frames_tk:
            return

        frame_image = self.gif_frames_tk[self.current_preview_frame_index]

        # 在 Canvas 中心绘制图像
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        # 清除旧图像（如果存在）
        self.preview_canvas.delete("frame")
        # 创建新图像
        self.preview_canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=frame_image, tags="frame")

        self.current_preview_frame_index = (self.current_preview_frame_index + 1) % len(self.gif_frames_tk)
        self.preview_job = self.after(self.animation_delay, self.animate_preview)


    def save_gif(self):
        """弹出保存对话框并保存 GIF 文件"""
        if not self.gif_frames_pil:
            messagebox.showwarning("未转换", "没有可保存的 GIF 数据。请先转换文件。")
            return

        # 从输入文件名生成默认输出文件名
        input_dir, input_filename = os.path.split(self.input_filepath)
        default_gif_name = os.path.splitext(input_filename)[0] + ".gif"

        save_path = filedialog.asksaveasfilename(
            title="保存 GIF 文件",
            initialdir=input_dir, # 默认打开输入文件所在的目录
            initialfile=default_gif_name, # 默认文件名
            defaultextension=".gif",
            filetypes=[("GIF 文件", "*.gif")]
        )

        if save_path:
            self.update_status("正在保存 GIF...")
            try:
                # 保存 GIF
                self.gif_frames_pil[0].save(
                    save_path,
                    save_all=True,
                    append_images=self.gif_frames_pil[1:], # 添加剩余的帧
                    duration=self.animation_delay,        # 每帧的持续时间 (毫秒)
                    loop=0,                              # 0 表示无限循环
                    optimize=False,                      # 可以设为 True 尝试优化文件大小
                    transparency=0,                      # 使用第一帧的透明度信息
                    disposal=2                           # 关键：处理透明背景的关键，保留前一帧
                )
                self.update_status(f"GIF 已保存到: {save_path}")
                messagebox.showinfo("保存成功", f"GIF 文件已成功保存到:\n{save_path}")
            except Exception as e:
                self.update_status(f"保存失败: {e}")
                messagebox.showerror("保存失败", f"保存 GIF 时发生错误:\n{e}")
            finally:
                # 可以在这里决定保存后是否禁用保存按钮，通常不需要
                pass


if __name__ == "__main__":
    app = SpriteSheetConverter()
    app.mainloop()
