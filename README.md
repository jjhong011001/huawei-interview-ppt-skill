# Huawei Interview PPT Skill

一个面向华为不同岗位的 Codex skill。根据目标岗位、真实简历和项目材料规划中文面试 PPT，编写逐页讲稿，并配合 `presentations` skill 制作可编辑的 PPTX。

## 安装

将本仓库克隆到 Codex 技能目录：

```bash
git clone https://github.com/jjhong011001/huawei-interview-ppt-skill.git ~/.codex/skills/huawei-interview-ppt
```

然后在 Codex 中调用 `$huawei-interview-ppt`。如果已经有同名技能目录，请先选择另一个安装路径或处理现有目录。

## 使用示例

> 用 $huawei-interview-ppt，参考我的简历、项目介绍、华为目标岗位 JD 和这份 PPT 模板，先规划每页内容，再制作可编辑 PPT 并写好逐页讲稿。

这个 skill 不预设部门、岗位或页数。建议提供目标岗位、简历、项目材料，以及希望沿用的模板或成稿。缺少图片时可以先保留可替换位置。

`scripts/extract_materials.py` 可从 `.md`、`.tex`、`.txt` 中摘取带行号的材料片段：

```bash
python3 scripts/extract_materials.py resume.tex projects.md --output /tmp/materials.json
```

`scripts/check_deck.py` 可检查 PPTX 结构、讲稿备注和未处理的文字占位符：

```bash
python3 scripts/check_deck.py interview.pptx --min-slides 1
```

脚本只做机械检查。事实、职责归属和视觉排版仍需结合原始材料与逐页渲染结果核对。制作 PPT 时需要可用的 `presentations` skill。

## 商标与个人材料

本仓库不包含华为标志、个人简历、证书、照片或现成面试 PPT。使用者应提供自己有权使用的素材。华为及其标志属于相应权利人，本项目与华为没有官方关联。

## 许可证

代码和文字说明采用 [MIT License](LICENSE)。
