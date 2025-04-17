# Sprite Sheet to GIF 转换器

一个简单易用的工具，用于将4x4序列贴图（精灵表）转换为GIF动画。

## 功能特点

- 支持将4x4排列的PNG序列贴图转换为GIF动画
- 直观的图形用户界面
- 支持文件拖放操作
- 实时GIF预览功能
- 支持透明背景
- 自动处理帧动画

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

1. 将4x4排列的PNG序列图拖放到应用程序窗口，或点击"浏览"按钮选择文件
2. 点击"转换为GIF"按钮
3. 预览生成的GIF动画
4. 点击"保存GIF"按钮将动画保存到本地

## 注意事项

- 输入图像必须是4x4排列的序列贴图
- 图像尺寸必须能被4整除
- 支持透明背景

## 构建可执行文件

如果你想构建独立的可执行文件，可以使用PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed sprite_to_gif.py
```

## 贡献

欢迎提交问题和改进建议！

## 许可证

本项目采用MIT许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 作者

RusianHu
