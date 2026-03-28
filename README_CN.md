# MineSR: Minecraft 超分辨率数据集

> 数据集正在制作中，完毕后会上传链接。

<p align="center">
  <a href="README.md">English</a> | <a href="README_CN.md">简体中文</a>
</p>

## 概述
本仓库提供了制作 **MineSR 数据集** 的自动化脚本。MineSR 数据集旨在提供 Minecraft 高分辨率（1080P，通过模组获取）与低分辨率（270P，通过原版截图获取）成对图像，以支持超分辨率模型训练。

为了确保训练样本间的退化一致性，我们使用单一下采样策略，即利用 Resolution Control 模组修改 Buffer Size 以获取 HR（高分辨率图像）。

### 核心流程
MineSR 的脚本化流程核心包含三步：

1. **生成任务**：使用 `generate.py` 生成带群系标签或手动坐标生成的采集任务 JSON。
2. **区块预加载**：使用 `maprun.py` 按任务点预加载区块，减少区块渲染延迟。
3. **自动化采集**：使用 `capture.py` 自动执行传送与截图，输出可用于数据集构建的样本。

进行区块预加载或自动截图时，Minecraft 需要保持为主窗口，这意味着脚本运行时不能同时进行其他前台操作。
### 项目结构

- `generate.py`：从 `biomes_x_x_x.csv` 或 `coords_x_x_x.csv` 生成`capture_list_x_x_x.json`。
- `maprun.py`：按 `capture_list_x_x_x.json` 在游戏通过传送预加载区块。
- `capture.py`：按 `capture_list_x_x_x.json` ，执行天气/时间/传送并触发截图热键，记录采集日志。
- `utils/config_loader.py`：YAML 配置加载器。
- `utils/window_resize.py`：基于 Win32 API 的 Minecraft 窗口客户区尺寸调整。
- `utils/logger_utils.py`：公共 logger。
- `configs/generate_x_x_x.yaml`：x.x 版本的生成配置。
- `configs/capture_x_x_x.yaml`：x.x 版本的采集阶段配置。
- `data/biomes_x_x_x.csv`：**手动**编写的群系坐标输入（`biome,x,z`）。
- `data/coords_x_x_x.csv`：**手动**任务输入（可选）。
- `data/capture_list_x_x_x.json`：`generate.py` **生成**的任务文件，供 maprun/capture 脚本使用。

## 说明

我暂时不考虑使用第三方地图，或是针对全方块、物品、生物专门进行截图。
如果您愿意让我使用您的光影，我很乐意使用它来做相应光影版本的数据集。

有问题欢迎随时邮箱联系我。`rayzeros@e.gzhu.edu.cn`

---

## 数据集规划
*计划中的条目随时可能发生变化*

| 版本号 | 版本信息| 图片数量 | 情况 |
|:-----:|-------|:-----:|:-----:|
| 1.0 | 主世界**地表**的所有群系(46个)| 1840 | 进行中🛠️ |
| 1.1 | 添加主世界**地底**的3个群系*100对、主世界Features| / | 计划中📅 |
| 1.2 | 添加主世界**地表**所有群系的雨/雪天情景| / | 计划中📅 |
| 2.0 | 添加地狱的5个群系*50、地狱的Features| / | 计划中📅 |
| 3.0 | 添加末地主岛与外岛、末地的Features | / | 计划中📅 |

---

## 使用信息与环境配置

- [[ 官网 ]](https://www.minecraft.net) **游戏版本** Minecraft 1.20.1
- [[ 官网 ]](https://fabricmc.net/) **模组加载器** Fabric 0.18.2

**模组列表：**
- [[ Resolution Control ]](https://github.com/UltimateBoomer/Resolution-Control) resolution-control-plus-1.20-3.0.0
- [[ ModMenu ]](https://github.com/TerraformersMC/ModMenu) modmenu-7.2.2
- [[ Sodium Extra ]](https://github.com/FlashyReese/sodium-extra) sodium-extra-0.5.9+mc1.20.1
- [[ Sodium ]](https://github.com/CaffeineMC/sodium) sodium-fabric-0.5.13+mc1.20.1
- [[ Reese's Sodium Options ]](https://github.com/FlashyReese/reeses-sodium-options) reeses_sodium_options-1.7.2+mc1.20.1-build.101
- [[ Fabric API ]](https://github.com/FabricMC/fabric-api) fabric-api-0.92.6+1.20.1
- [[ Iris ]](https://github.com/IrisShaders/Iris) iris-1.7.6+mc1.20.1


<details>
<summary><b>Minecraft 相关设置</b></summary>

- 通用
    - 渲染距离 16 区块
    - 模拟距离 12 区块
    - 亮度 50%
- Quality
    - 图像品质 高品质
    - Color Space: sRGB
    - 云 高品质
    - 天气 默认
    - Leaves 默认
    - 粒子效果 全部
    - 平滑光照 开启
    - 生物群系过渡距离 2 blocks
    - 实体渲染距离 100%
    - 实体阴影 开启
    - Vignette 开启
    - 屏幕扭曲效果 100%
    - 视场角效果 100%
    - Mipmap 等级 4x
- Performance
    - Use Fog Occlusion 开启
- 动画
    - 全部 开启
- 粒子效果
    - 全部 开启
- 细节 全部开启
- 显示
    - 多维度迷雾 关
    - 迷雾起始点 100%
    - 全局迷雾 默认
    - 光照更新 默认
    - 以下均开启：物品展示框、盔甲架、画、信标光柱、附魔台上的书、活塞、物品展示框名称标签、玩家名称标签
    - 限制信标光柱高度 关闭
- 其他
    - 云层高度 192
    - 云层距离 100 %
</details>
&nbsp;

**运行环境(供参考)**：
- Windows（`window_resize.py` 依赖 Win32 API）
- Python 3.9+ （测试环境为 3.13.5）
- OpenJDK 17 (或 Oracle Java 17) ——*Minecraft 1.20.1 运行所需*

**依赖安装**:
```bash
python -m pip install pyautogui pyyaml
```

**功能声明与免责：**
本项目未对任何上述模组的源代码进行修改或分发。其中 Fabric API 用作模组基础库，Iris、Sodium、Sodium Extra 用于提供更多的视觉与性能选项，ModMenu 与 Reese's Sodium Options 用于优化 UI 交互，Resolution Control 用于截图。

**Minecraft 免责声明：**
本项目为第三方开源工具，与 Mojang Studios 无关联，且未获得 Mojang Studios 的官方认可。Minecraft 的名称、商标及所有相关游戏资产版权均归 Mojang Studios 所有。本项目严格遵守 Minecraft [最终用户许可协议 (EULA)](https://account.mojang.com/documents/minecraft_eula)。


---

## 使用指南

### 1. YAML 配置与命令行覆盖

项目支持通过 YAML 配置文件进行参数管理，位于 `./configs/` 目录下。
数据集版本更新可能会新增对应的 YAML 文件，您可以将其视作“增量”配置文件独立运行。

- `./configs/capture_1_0_0.yaml`
- `./configs/generate_1_0_0.yaml`

### 2. 运行示例：
可以运行仓库已有的配置文件

- **生成任务**
```bash
python generate.py --config configs/generate_1_0_0.yaml
```
- **区块预加载**
```bash
python maprun.py
```
- **自动化采集**
```bash
python capture.py --config configs/capture_1_0_0.yaml
```

可以通过命令行覆盖 YAML 默认值，示例：

```bash
python generate.py --config ./configs/generate_1_0_0.yaml --total-samples 1840 --seed 42 --output-file ./data/capture_list_1_0_0.json
python capture.py --config ./configs/capture_1_0_0.yaml --wait-time 2.0 --lr-res 480 270 --input-file ./data/capture_list_1_0_0.json
```
> [!NOTE]
> `maprun.py` 没有独立配置文件，需要手动修改代码中的 `INPUT_FILE` 指向目标 `capture_list_x_x_x.json`。
> 因此如果你修改了 `generate_x_x_x.yaml` 的 `output_file`，请同步修改 `maprun.py`。

### 3. 配置说明

#### 3.0 前置准备

部分配置参数与采样任务过程无直接关联，但需要手动填写/更改，以记录在生成文件中。

> [!IMPORTANT]
> **前置准备**：这些配置参数不与采样过程直接相关，但务必在运行前手动填写至 `configs/*.yaml` 中，以确保生成文件元数据完整。
> 尽管这些参数在下面会再次提及，但请务必将它们正确记录在对应的配置文件中。
>
> 1. 在 Minecraft 中创建新世界，使用 `/seed` 指令查询并将种子填入 `generate_x_x_x.yaml` 作为记录。
> 2. 在 Resolution Control 模组中设置截图快捷键，并将该键位写入 `capture_x_x_x.yaml` 的 `mod_key`。
>    在模组菜单的 Screenshot 页面中，设置截图分辨率（高分辨率），记为 `hr_res` 并写入 `capture_x_x_x.yaml`。
> 3. 请确保 Minecraft 文件夹中有screenshots文件夹，否则 Resolution Control 模组截图会导致崩溃。


#### 3.1 生成配置（`configs/generate_x_x_x.yaml`）
- `total_samples`（int）：总样本数，即采样多少对截图。
- `seed`（int）：地图种子，**仅做日志作用，需要手动填写**。
- `enable_y`（bool）：是否输出 Y 轴。启用时输出将包含 `y` 字段。此选项影响 `enable_manual`。
- `random_y`（bool）：是否启用随机生成 Y 轴数值。启用时使用 `/tp` 逻辑，需要为所需坐标手动填写，未填写部分/关闭时使用 `/execute positioned ... over ocean_floor ...` 逻辑。此选项不影响 `enable_manual`。
- `enable_manual`（bool）：
	- `true`：从 `manual_csv_file` 读取。
	- `false`：从 `biomes_csv_file` 自动生成。
    你只需提供对应模式所需的一个文件。
- `biomes_csv_file`（str）：群系中心输入 CSV（`biome,x,z`）。
- `manual_csv_file`（str）：手动任务输入 CSV（`id,biome,yaw,pitch,time,x,z[,y]`）。
- `coordinate_offset`（int）：自动生成时中心点随机偏移半径（`±offset`）。
- `yaw_range`（int_pair）：yaw 随机范围。
- `pitch_range`（int_pair）：pitch 随机范围。
- `time_points`（str）：可选时间点，逗号分隔。
- `output_file`（str）：输出 JSON 路径。

`generate.py` 读取配置后，生成的 JSON 的 `config` 中会记录：

- `total_samples`、`enable_y`、`random_y`、`enable_manual`、`seed`、`coordinate_offset`、`yaw_range`、`pitch_range`、`time_points`
- 并根据模式仅保留一个来源字段：
	- 手动模式：`manual_csv_file`
	- 自动模式：`biomes_csv_file`

#### 3.2 采集配置（`configs/capture_x_x_x.yaml`）
- `input_file`（str）：输入任务 JSON。
- `log_suffix`（str）：采集日志输出路径与文件名后缀。
- `lr_res`（int_pair）：窗口目标分辨率。
- `hr_res`（int_pair）：高分辨率值，**仅做日志作用，需要在 Resolution Control 菜单手动填写**
- `wait_time`（float）：每条样本截图前等待时间。用于等待区块加载，若机器性能较好可以适量减小。
- `mod_key`（str）：Resolution Control 截图热键。
- `mc_key`（str）：Minecraft 截图热键。

#### 3.3 预加载配置（`maprun.py`）

- `INPUT_FILE`：输入 `capture_list_x_x_x.json` 任务文件
- `WAIT_TIME`：加载区块等待时间
- `LOG_SUFFIX`：日志文件输出位置与文件后缀

---

### 4. 数据格式

#### 4.1 群系中心 `data/biomes_x_x_x.csv`

表头顺序固定：

```csv
biome,x,z
```
_你可以使用一些种子查看器来搜寻群系坐标，从而更方便地编写此文件。_

#### 4.2 手动任务 `data/coords_x_x_x.csv`

`enable_y=false` 时：

```csv
id,biome,yaw,pitch,time,x,z
```
`enable_y=true` 时：

```csv
id,biome,yaw,pitch,time,x,z,y
```
_对难以自动生成的位置（如洞穴）可使用手动任务。_

#### 4.3 任务 JSON

顶层结构（示例）：

```json
{
    "config": { ... },
    "coords": [
        {
            "id": 0,
            "biome": "plain",
            "yaw": -93.79,
            "pitch": 20.02,
            "time": 13000,
            "x": -18307,
            "z": -6911
        }
    ]
}
```

若 `enable_y=true`，每条记录会额外包含 `y` 字段。

---

### 5. 复现建议

**如果你需要复现此数据集**，请根据版本选取对应的配置文件，同步指示的环境配置。以 1.0 版本为例：
```bash
# 利用 biomes_1_0_0.csv 生成 capture_list_1_0_0.json
python generate.py --config configs/generate_1_0_0.yaml
# (可选，需要主窗口为Minecraft）预加载区块
python maprun.py
# (需要主窗口为Minecraft) 执行截图
python capture.py --config configs/capture_1_0_0.yaml
```
截图会保存在 Minecraft 对应文件夹的 screenshots 文件夹中，mod截图带有`fb`前缀，如 `fb2026-03-25_19.46.17.png`，原版截图形如 `2026-03-10_15.14.38.png`，建议备份并清空该文件夹，按时间顺序重命名“截图对”。

**如果你需要制作数据集，建议**：
- 固定 `seed` 以保证随机生成可复现。
- 发布数据集时一并保留对应版本配置文件（如 `*_1_0_0.yaml`）。
- 保留最终用于采集的任务 JSON，便于溯源。

## 关于数据集复现

不同于专门的渲染引擎，由于游戏环境的动态特性，我们难以控制Minecraft的frametime等变量，这可能会使得Minecraft的动画播放、基于frametime的计算（一些shaderpacks）等事件，在尝试复现时存在差异：例如云层飘动、雨滴效果、熔岩动画。
使用 `/execute positioned x 0 z positioned over ocean_floor run tp @s ~ ~ ~` 指令可以替代 `/spreadplayers` 以传送玩家至实体方块上，避免后者拒绝操作导致的一系列问题。
`random_y`的作用现在变为允许随机生成`x,z`坐标时，手动控制一部分坐标的`y`轴。你需要启用 `enable_y` 且禁用 `random_y`，这样生成的`y`坐标均为`null`，配合`/execute`指令传送至最高的实体方块上，此时你可以为那些~~原本会卡在方块中/漂浮中的传送点/~~洞穴或其他地表以外的位置，手动寻找一个安全的`y`值，并改动 `json` 文件中的 `coords` 项。
我使用的方法是游戏内截图（F2）与 Mod 截图，但 `pyautogui.hotkey()` 并不能使得这两条指令在机器上严谨的同时发生，正在运作的渲染管线本身也不支持此逻辑，因此实际运行时HR与LR难以保持绝对一致，虽然在静态场景上几乎无影响（比如daytime会有差异），但动态场景（尤其是雨滴效果）则可能会比较明显。这会为退化模型引入一定的随机性，因此相比较于使用下采样算法，采集方法本身与游戏特性会导致我的数据集本身难以完全复现。~~但我认为LR-HR对的随机差异客观上可以增加退化模型构建的复杂性，以提升模型面对复杂动态场景时的鲁棒性。~~

虽然我使用 <https://github.com/UltimateBoomer/Resolution-Control> 作为了第二个截图方法，但我也对这个项目的1.20分支进行了魔改，使其能够在截图后的下一帧，继续进行相应分辨率的截图，从而达到近似“同时获取”的效果，经过测试，这个方案与这个项目的方案（混合原版截图）没有明显差距，详细来说，Minecraft的雨滴下落依旧不能在两张图像对应，这是一个根本性的问题。
不过这个魔改还是可以让你的截图变得更优雅，或许你正好有这个需求，亦或是与某些点不谋而合。你可以在这里获取： <https://github.com/Ray-Zeros/Resolution-Control>