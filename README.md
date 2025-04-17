# Sprite Sheet to GIF 转换器

一个简单易用的工具，用于将序列贴图（精灵表）转换为GIF动画。支持4x4和3x4两种格式的序列贴图。

## 功能特点

- 支持将4x4和3x4排列的PNG序列贴图转换为GIF动画
- 直观的图形用户界面
- 支持文件拖放操作
- 实时GIF预览功能
- 支持透明背景
- 自动处理帧动画
- 可选择不同的序列贴图格式

## 截图

(这里可以添加应用程序的截图)

## 安装要求

- Python 3.6+
- 依赖库:
  - Pillow (PIL)
  - tkinterdnd2

## 安装方法

1. 克隆或下载此仓库
2. 安装所需依赖:

```bash
pip install Pillow tkinterdnd2
```

## 使用方法

运行主程序:

```bash
python sprite_to_gif.py
```

### 使用步骤:

1. 选择序列贴图格式（4x4或3x4）
2. 将PNG序列图拖放到应用程序窗口，或点击"浏览"按钮选择文件
3. 点击"转换为GIF"按钮
4. 预览生成的GIF动画
5. 点击"保存GIF"按钮将动画保存到本地

## 注意事项

- 输入图像必须是4x4或3x4排列的序列贴图
- 支持透明背景
- 程序会自动计算每个帧的尺寸

## 可执行文件

如果你想自己构建可执行文件，可以使用PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed sprite_to_gif.py
```

## 贡献

欢迎提交问题和改进建议！

## 许可证

本项目采用MIT许可证 - 详情请查看 [LICENSE](LICENSE) 文件
