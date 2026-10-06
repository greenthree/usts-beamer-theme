# USTS Beamer Theme

[![Build example](https://github.com/greenthree/usts-beamer-theme/actions/workflows/build.yml/badge.svg)](https://github.com/greenthree/usts-beamer-theme/actions/workflows/build.yml)

一份面向苏州科技大学师生的非官方通用 Beamer 模板，适用于课程汇报、学术报告、项目展示和竞赛讲解。

模板从一份校内程序设计竞赛题解幻灯片中提取并整理，保留了原稿的学校蓝、通栏标题、圆角阴影信息块和分段页脚，同时修正了导航符号未关闭等问题，并补充了更适合复用的标题页、章节页和页脚选项。

![模板预览](preview.png)

## 配色

| 名称 | RGB | HEX | 用途 |
| --- | --- | --- | --- |
| USTS Blue | `0, 140, 215` | `#008CD7` | 主标题、结构色 |
| USTS Deep Blue | `0, 105, 161` | `#0069A1` | 信息块标题、页脚 |
| USTS Dark Blue | `0, 70, 108` | `#00466C` | 深色页脚、重点信息 |
| USTS Light Blue | `229, 240, 246` | `#E5F0F6` | 信息块背景 |

## 快速开始

1. 下载或克隆仓库。
2. 将 `beamerthemeUSTS.sty`、`beamercolorthemeUSTS.sty` 和 `assets/` 放在你的 `.tex` 文件旁边。
3. 在导言区加载主题：

```tex
\documentclass[aspectratio=169,11pt]{beamer}
\usepackage[UTF8]{ctex}
\usepackage{graphicx}
\usetheme[footline=full]{USTS}

\title[报告简称]{报告标题}
\author[姓名]{姓名}
\institute[USTS]{学院或部门\\苏州科技大学}
\date{\today}
\titlegraphic{\includegraphics[height=1.25cm]{assets/usts-logo.jpg}}
```

仓库中的中文示例使用 **XeLaTeX** 编译，CI 也使用该引擎。不要使用 pdfLaTeX 编译 `example.tex`：其中的中文 `listings` 示例不兼容 pdfLaTeX。LuaLaTeX 也可编译，但字体配置可能需要按本机环境调整。

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error example.tex
```

完整用法见 [`example.tex`](example.tex)。

## 常用语法示例

`example.tex` 现在覆盖以下常见场景：

- 单张图片、图注、等比例缩放；
- 图文双栏、图片裁剪与对齐；
- 公式、表格、普通块、示例块和提醒块；
- 定义、定理与证明环境；
- 使用覆盖层逐步显示内容；
- Python 代码高亮；
- 外部链接、Beamer 按钮和页内跳转。

插入自己的图片时，可直接使用：

```tex
\begin{figure}
  \centering
  \includegraphics[
    width=0.7\linewidth,
    keepaspectratio
  ]{assets/image-file.jpg}
  \caption{图片说明}
\end{figure}
```

需要裁剪时使用 `trim = left bottom right top`，并同时加入 `clip`：

```tex
\includegraphics[
  width=\linewidth,
  trim=18 18 18 18,
  clip
]{assets/image-file.jpg}
```

示例中的 `example-image-a` 和 `example-image-b` 来自 TeX Live 的 `mwe` 宏包，仅用于演示图片布局；实际使用时替换为自己的图片即可。

## 页脚选项

主题提供三种页脚模式：

```tex
\usetheme[footline=full]{USTS}    % 作者 / 标题 / 日期 / 页码
\usetheme[footline=minimal]{USTS} % 标题 / 页码
\usetheme[footline=none]{USTS}    % 不显示页脚
```

页脚采用单行布局，超长文字会等比例缩小到所属分栏。为了投影时保持清晰，建议为较长的报告名、作者列表和日期提供简写：

```tex
\title[项目汇报]{一份完整的项目研究与成果汇报标题}
\author[绿化三等]{绿化三 \and 李四 \and 王五}
\institute[USTS]{物理科学与技术学院\\苏州科技大学}
\date[2026-10]{2026 年 10 月}
```

未设置 `\institute`，或使用 `\institute[]{完整单位名称}` 时，页脚不显示单位及括号。只写 `\institute{完整单位名称}` 时，Beamer 会将完整名称同时用于页脚。

## 文件结构

```text
.
├── beamerthemeUSTS.sty       # 布局、字体、标题页与页脚
├── beamercolorthemeUSTS.sty  # 颜色定义
├── example.tex               # 中文示例
├── assets/
│   ├── usts-logo.jpg
│   └── README.md
├── tests/                    # 排版边界情况与 PDF 检查
└── .github/workflows/build.yml
```

## 自定义

主题加载后，可以使用标准 Beamer 接口覆盖颜色和字体。例如：

```tex
\setbeamerfont{frametitle}{size=\Large,series=\bfseries}
\setbeamercolor{alerted text}{fg=USTSDarkBlue}
```

如果需要自动章节页，可在导言区加入：

```tex
\AtBeginSection[]{
  \begin{frame}[plain]
    \sectionpage
  \end{frame}
}
```

Beamer 页码统计的是 frame，逐步显示产生的多个 PDF 页面共用一个 frame 编号。默认情况下，封面与章节页也参与计数；`plain` 只隐藏页眉和页脚。若希望封面或章节页不参与计数，将对应页面写为 `\begin{frame}[plain,noframenumbering]`。

标题栏会随长标题和副标题自然增高，左右缩进随 `\setbeamersize` 设置的正文边距变化。若需要更醒目的提醒块，可用标准 Beamer 接口设置辅色：

```tex
\setbeamercolor{alerted text}{fg=orange!85!black}
\setbeamercolor{block title alerted}{fg=white,bg=orange!85!black}
\setbeamercolor{block body alerted}{fg=black,bg=orange!10!white}
```

## 排版回归检查

在仓库根目录运行以下命令（PDF 检查需要 Python 3 和 Poppler 的 `pdftotext`）：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error tests/regression.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error tests/regression-43.tex
python tests/check_pdf.py regression.pdf regression-43.pdf
```

回归示例覆盖空单位、完整单位与简写单位、长标题自动换行、手动换行、副标题，以及完整、极简、无页脚模式。CI 会检查 16:9 和 4:3 两种比例中标题是否完整、文字是否位于页面内，以及页脚是否越过分栏边界。

## 许可与声明

主题代码以 [MIT License](LICENSE) 开源。

本项目是社区维护的非官方模板，与苏州科技大学官方无隶属或授权关系。“苏州科技大学”名称、校徽及相关标识的权利归其各自权利人所有；校徽文件不因本项目采用 MIT License 而改变其权利归属。使用者应遵守学校的视觉标识规范。

欢迎提交 Issue 或 Pull Request 改进兼容性、示例和文档。

---

Unofficial Beamer theme for Suzhou University of Science and Technology (USTS). Compile the Chinese example with XeLaTeX.
