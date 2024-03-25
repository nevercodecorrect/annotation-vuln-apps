<!-- DO NOT EDIT THIS FILE DIRECTLY. INSTEAD EDIT THE `readme_template.md` OR `guides/1)getting_started/1)quickstart.md` TEMPLATES AND THEN RUN `render_readme.py` SCRIPT. -->

<div align="center">

[<img src="../gradio.svg" alt="gradio" width=400>](https://gradio.app)<br>
<em>轻松构建 & 分享 令人愉快的机器学习程序</em>

[![gradio-backend](https://github.com/gradio-app/gradio/actions/workflows/backend.yml/badge.svg)](https://github.com/gradio-app/gradio/actions/workflows/backend.yml)
[![gradio-js](https://github.com/gradio-app/gradio/actions/workflows/ui.yml/badge.svg)](https://github.com/gradio-app/gradio/actions/workflows/ui.yml)  
 [![PyPI](https://img.shields.io/pypi/v/gradio)](https://pypi.org/project/gradio/)
[![PyPI downloads](https://img.shields.io/pypi/dm/gradio)](https://pypi.org/project/gradio/)
![Python version](https://img.shields.io/badge/python-3.8+-important)
[![Twitter follow](https://img.shields.io/twitter/follow/gradio?style=social&label=follow)](https://twitter.com/gradio)

[官网](https://gradio.app)
| [文档](https://gradio.app/docs/)
| [指南](https://gradio.app/guides/)
| [开始](https://gradio.app/getting_started/)]
| [样例](../../demo/)
| [English](https://github.com/gradio-app/gradio#readme)

</div>

# Gradio: 用Python构建机器学习网页APP

Gradio是一个开源的Python库，用于构建演示机器学习或数据科学，以及web应用程序。

使用Gradio，您可以基于您的机器学习模型或数据科学工作流快速创建一个漂亮的用户界面，让用户可以”尝试“拖放他们自己的图像、粘贴文本、录制他们自己的声音，并通过浏览器与您的演示程序进行交互。

![Interface montage](../header-image.jpg)

Gradio适用于:

- 向客户/合伙人/用户/学生**演示**您的机器学习模型。

- 通过自动共享链接快速**部署**您的模型，并获得模型性能反馈。

- 在开发过程中使用内置的操作和解释工具交互式地**调试**模型。

### 快速开始

**依赖**: Gradio只需要Python 3.7及以上版本！

#### Gradio能做什么？

与他人共享机器学习模型、API或数据科学工作流程的最佳方法之一就是创建一个**交互式应用**，让用户或同事在他们的浏览器中试用。

Gradio让你可以**用Python构建演示并分享它们**，而且通常只需几行代码！下面让我们开始吧。

#### Hello, World

要用Gradio运行"Hello World"示例，需要以下三个步骤：

1\. 用pip下载Gradio:

```bash
pip install gradio
```

2\. 用Python脚本或在Jupyter Notebook中运行下面的代码 （或者使用 [Google Colab](https://colab.research.google.com/drive/18ODkJvyxHutTN0P5APWyGFO_xwNcgHDZ?usp=sharing)）:

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

3\. 下面的演示会自动出现在Jupyter Notebook中，如果使用脚本运行则会在浏览器[http://localhost:7860](http://localhost:7860)弹出:

![`hello_world` demo](../../demo/hello_world/screenshot.gif)

#### `Interface` 类

你可能会注意到，在运行示例时我们创建了一个 `gradio.Interface` 。 `Interface` 类可以用用户接口包装任意的Python函数。在上面的示例中，我们使用了一个基于文本的简单函数，但这个函数可以是任何东西，从音乐生成器到税率计算器，再到预训练机器学习模型的预测函数。

`Interface` 类核心需要三个参数初始化：

- `fn` : 被UI包装的函数
- `inputs` : 作为输入的组件 (例如： `"text"`, `"image"` or `"audio"`)
- `outputs` : 作为输出的组件 (例如： `"text"`, `"image"` or `"label"`)

下面我们进一步分析用于输入和输出的组件。

#### 组件属性

在之前的示例中我们可以看到一些简单的文本框组件 `Textbox` ，但是如果您想改变UI组件的外观或行为呢?

假设您想要自定义输入文本字段，例如您希望它更大并有一个文本占位符。如果我们使用 `Textbox` 的实际类，而不是使用字符串快捷方式，就可以通过组件属性实现个性化。

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(lines=2, placeholder="Name Here..."),
    outputs="text",
)
demo.launch()
```

![`hello_world_2` demo](../../demo/hello_world_2/screenshot.gif)

#### 多输入和输出组件

假设您有一个更复杂的函数，有多个输入和输出。在下面的示例中，我们定义了一个函数，该函数接受字符串、布尔值和数字，并返回字符串和数字。观察应该如何传递输入和输出组件列表。

```python
import gradio as gr

def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
)
demo.launch()
```

![`hello_world_3` demo](../../demo/hello_world_3/screenshot.gif)

您只需将组件包装在列表中。输入列表`inputs`中的每个组件依次对应函数的一个参数。输出列表`outputs`中的每个组件都对应于函数的一个返回值，两者均按顺序对应。

#### 一个图像示例

Gradio支持多种类型的组件，如 `Image`、`DateFrame`、`Video`或`Label` 。让我们尝试一个图像到图像的函数来感受一下！

```python
import numpy as np
import gradio as gr

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gr.Interface(sepia, gr.Image(shape=(200, 200)), "image")
demo.launch()
```

![`sepia_filter` demo](../../demo/sepia_filter/screenshot.gif)

当使用`Image`组件作为输入时，您的函数将接收一个形状为 `(height, width, 3)` 的NumPy数组，其中最后一个维度表示RGB值。我们还将以NumPy数组的形式返回一张图像。

你也可以用 `type=` 关键字参数设置组件使用的数据类型。例如，如果你想让你的函数获取一个图像的文件路径，而不是一个NumPy数组时，输入 `Image` 组件可以写成：

```python
gr.Image(type="filepath", shape=...)
```

还要注意，我们的输入 `Image` 组件带有一个编辑按钮 🖉，它允许裁剪和放大图像。以这种方式操作图像可以帮助揭示机器学习模型中的偏见或隐藏的缺陷！

您可以在[Gradio文档](https://gradio.app/docs)中阅读更多关于组件以及如何使用它们。

#### Blocks: 更加灵活且可控

Gradio 提供了两个类来构建应用程序

1\. **Interface**，这为创建到目前为止我们一直在讨论的示例提供了一个高级抽象。

2\. **Blocks**，一个用于设计具有更灵活布局和数据流的web应用程序的初级API。block可以做许多事，比如特征化多个数据流和演示，控制组件在页面上出现的位置，处理复杂的数据流（例如，输出可以作为其他函数的输入），以及根据用户交互更新组件的属性/可见性，且仍然在Python中。如果您需要这种个性化，那就试试 `Blocks` 吧！

#### 你好, Blocks

让我们看一个简单的例子。注意这里的API与 `Interface` 有何不同。

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=name, outputs=output)

demo.launch()
```

![`hello_blocks` demo](../../demo/hello_blocks/screenshot.gif)

注意事项：

- `Blocks` 由 `with` 子句组成，在该子句中创建的任何组件都会自动添加到应用程序中。
- 组件在应用程序中按创建的顺序垂直显示，（稍后我们将介绍自定义布局！）
- 一个 按钮 `Button` 被创建，然后添加了一个 `click` 事件监听器。这个API看起来很熟悉！就像 `Interface`一样， `click` 方法接受一个Python函数、输入组件和输出组件。

#### 更多复杂性

这里有一个应用程序可以让你感受一下`Blocks`的更多可能：

```python
import numpy as np
import gradio as gr

def flip_text(x):
    return x[::-1]

def flip_image(x):
    return np.fliplr(x)

with gr.Blocks() as demo:
    gr.Markdown("Flip text or image files using this demo.")
    with gr.Tabs():
        with gr.TabItem("Flip Text"):
            text_input = gr.Textbox()
            text_output = gr.Textbox()
            text_button = gr.Button("Flip")
        with gr.TabItem("Flip Image"):
            with gr.Row():
                image_input = gr.Image()
                image_output = gr.Image()
            image_button = gr.Button("Flip")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

demo.launch()
```

![`blocks_flipper` demo](../../demo/blocks_flipper/screenshot.gif)

还有很多事情可以做！我们将在[使用blocks构建](https://gradio.app/building_with_blocks)部分为您介绍如何创建像这样复杂的 `Blocks` 应用程序。

恭喜你，你现在已经熟悉了Gradio的基础使用！🥳 去我们的[下一章](https://gradio.app/key_features) 了解Gradio的更多功能。

## 开源栈

Gradio是由许多很棒的开源库构建的，请一并支持它们!

[<img src="../huggingface_mini.svg" alt="huggingface" height=40>](https://huggingface.co)
[<img src="../python.svg" alt="python" height=40>](https://www.python.org)
[<img src="../fastapi.svg" alt="fastapi" height=40>](https://fastapi.tiangolo.com)
[<img src="../encode.svg" alt="encode" height=40>](https://www.encode.io)
[<img src="../svelte.svg" alt="svelte" height=40>](https://svelte.dev)
[<img src="../vite.svg" alt="vite" height=40>](https://vitejs.dev)
[<img src="../pnpm.svg" alt="pnpm" height=40>](https://pnpm.io)
[<img src="../tailwind.svg" alt="tailwind" height=40>](https://tailwindcss.com)

## 协议

Gradio is licensed under the Apache License 2.0 found in the [LICENSE](LICENSE) file in the root directory of this repository.

## 引用

另外请参阅论文 _[Gradio: Hassle-Free Sharing and Testing of ML Models in the Wild](https://arxiv.org/abs/1906.02569), ICML HILL 2019_，如果您在工作中使用Gradio请引用它。

```
@article{abid2019gradio,
  title = {Gradio: Hassle-Free Sharing and Testing of ML Models in the Wild},
  author = {Abid, Abubakar and Abdalla, Ali and Abid, Ali and Khan, Dawood and Alfozan, Abdulrahman and Zou, James},
  journal = {arXiv preprint arXiv:1906.02569},
  year = {2019},
}
```