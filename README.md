# MineSR: Minecraft Super-Resolution Dataset

> The dataset is currently in production. A link will be uploaded upon completion.

<p align="center">
  <a href="README.md">English</a> | <a href="README_CN.md">简体中文</a>
</p>

## Overview
This repository provides automated scripts for creating the **MineSR Dataset**. The MineSR dataset aims to provide paired high-resolution (1080P, acquired via mod) and low-resolution (270P, acquired via vanilla screenshots) images of Minecraft to support the training of super-resolution models.

To ensure consistent degradation between training samples, we use a single rendering-scale strategy: using the Resolution Control mod to modify Buffer Size and obtain HR (high-resolution) images.

### Core Workflow
The script-based workflow for MineSR consists of three core steps:

1. **Task Generation**: Use `generate.py` to generate a task JSON file containing biome labels or manually designated coordinates for capture.
2. **Chunk Preloading**: Use `maprun.py` to preload chunks at task coordinates via teleportation, reducing chunk rendering delays.
3. **Automated Capture**: Use `capture.py` to automatically execute teleportation and take screenshots, outputting samples suitable for dataset construction.

When performing chunk preloading or automated screenshots, Minecraft must remain the active foreground window, meaning no other foreground operations can be performed while the scripts are running.

### Project Structure

- `generate.py`: Generates `capture_list_x_x_x.json` from `biomes_x_x_x.csv` or `coords_x_x_x.csv`.
- `maprun.py`: Preloads chunks in the game via teleportation according to `capture_list_x_x_x.json`.
- `capture.py`: Executes weather/time changes, teleportation, and triggers screenshot hotkeys based on `capture_list_x_x_x.json`, logging the capture process.
- `utils/config_loader.py`: YAML configuration loader.
- `utils/window_resize.py`: Minecraft window client area resizing based on Win32 API.
- `utils/logger_utils.py`: public logger.
- `utils/check_spread.py`: Verify /spreadplayers execution via Minecraft latest.log.
- `configs/generate_x_x_x.yaml`: Generation configuration for version x.x.
- `configs/capture_x_x_x.yaml`: Capture-stage configuration for version x.x.
- `data/biomes_x_x_x.csv`: **Manual** Biome coordinate inputs (`biome,x,z`).
- `data/coords_x_x_x.csv`: **Manual** task inputs (optional).
- `data/capture_list_x_x_x.json`: Task file **generated** by `generate.py`, used by the maprun/capture scripts.

## Note

I am currently not considering using third-party maps, or taking screenshots specifically of full blocks, items, or mobs.
If you are willing to let me use your shaders, I would be happy to use them to create a corresponding shader-version dataset.

Feel free to email me if you have any questions. `rayzeros@e.gzhu.edu.cn`

---

## Dataset Roadmap
*Planned items are subject to change at any time*

| Version | Version Info | Image Count | Status |
|:-----:|-------|:-----:|:-----:|
| 1.0 | All biomes on the Overworld **Surface** (46) | 1840 | In Progress🛠️ |
| 1.1 | Add 3 Overworld **Underground** biomes * 100 pairs, Overworld Features | / | Planned📅 |
| 1.2 | Add Rain/Snow scenarios for all Overworld **Surface** biomes | / | Planned📅 |
| 2.0 | Add 5 Nether biomes * 50, Nether Features | / | Planned📅 |
| 3.0 | Add The End main island & outer islands, End Features | / | Planned📅 |

---

## Usage Information & Environment Setup

- [[ Official Site ]](https://www.minecraft.net) **Game Version** Minecraft 1.20.1
- [[ Official Site ]](https://fabricmc.net/) **Mod Loader** Fabric 0.18.2

**Mod List:**
- [[ Resolution Control ]](https://github.com/UltimateBoomer/Resolution-Control) resolution-control-plus-1.20-3.0.0
- [[ ModMenu ]](https://github.com/TerraformersMC/ModMenu) modmenu-7.2.2
- [[ Sodium Extra ]](https://github.com/FlashyReese/sodium-extra) sodium-extra-0.5.9+mc1.20.1
- [[ Sodium ]](https://github.com/CaffeineMC/sodium) sodium-fabric-0.5.13+mc1.20.1
- [[ Reese's Sodium Options ]](https://github.com/FlashyReese/reeses-sodium-options) reeses_sodium_options-1.7.2+mc1.20.1-build.101
- [[ Fabric API ]](https://github.com/FabricMC/fabric-api) fabric-api-0.92.6+1.20.1
- [[ Iris ]](https://github.com/IrisShaders/Iris) iris-1.7.6+mc1.20.1


<details>
<summary><b>Minecraft Settings</b></summary>

- General
    - Render Distance: 16 Chunks
    - Simulation Distance: 12 Chunks
    - Brightness: 50%
- Quality
    - Graphics: Fancy
    - Color Space: sRGB
    - Clouds: Fancy
    - Weather: Default
    - Leaves: Default
    - Particles: All
    - Smooth Lighting: ON
    - Biome Blend: 2 blocks
    - Entity Distance: 100%
    - Entity Shadows: ON
    - Vignette: ON
    - Distortion Effects: 100%
    - FOV Effects: 100%
    - Mipmap Levels: 4x
- Performance
    - Use Fog Occlusion: ON
- Animations
    - All: ON
- Particles
    - All: ON
- Details: ON for all
- Display
    - Multi-dimensional Fog: OFF
    - Fog Start: 100%
    - Global Fog: Default
    - The following are ON: Item Frames, Armor Stand, Painting, Beacon Beam, Enchanting Table Book, Piston, Item Frame Name Tag, Player Name Tag
    - Limit Beacon Beam Height: OFF
- Extras
    - Cloud Height: 192
    - Cloud Distance: 100%
</details>
&nbsp;

**Running Environment (for reference)**:
- Windows (`window_resize.py` depends on Win32 API)
- Python 3.9+ (Tested on 3.13.5)
- OpenJDK 17 (or Oracle Java 17) - *Required for Minecraft 1.20.1*

**Dependency Installation**:
```bash
python -m pip install pyautogui pyyaml
```

**Functionality Declaration & Disclaimer:**
This project does not modify or distribute the source code of any of the aforementioned mods. Fabric API is used as the mod base library. Iris, Sodium, and Sodium Extra provide more visual and performance options. ModMenu and Reese's Sodium Options optimize UI interaction. Resolution Control is used for taking screenshots.

**Minecraft Disclaimer:**
This project is a third-party open-source tool, not associated with Mojang Studios, and is not officially endorsed by Mojang Studios. The Minecraft name, trademarks, and all related game assets are copyright of Mojang Studios. This project strictly complies with the Minecraft [End User License Agreement (EULA)](https://account.mojang.com/documents/minecraft_eula).


---

## Usage Guide

### 1. YAML Configuration and Command Line Overrides

The project supports parameter management via YAML configuration files located in the `./configs/` directory.
Dataset version updates may add corresponding YAML files, which you can run independently as "incremental" configuration files.

- `./configs/capture_1_0_0.yaml`
- `./configs/generate_1_0_0.yaml`

### 2. Running Examples:
You can run the existing configuration files in the repository.

- **Task Generation**
```bash
python generate.py --config configs/generate_1_0_0.yaml
```
- **Chunk Preloading**
```bash
python maprun.py
```
- **Automated Capture**
```bash
python capture.py --config configs/capture_1_0_0.yaml
```

You can override YAML defaults via the command line. Example:

```bash
python generate.py --config ./configs/generate_1_0_0.yaml --total-samples 1840 --seed 42 --output-file ./data/capture_list.json
python capture.py --config ./configs/capture_1_0_0.yaml --wait-time 2.0 --lr-res 480 270 --input-file ./data/coords_list.json
```
> [!NOTE]
> `maprun.py` does not have an independent configuration file; you need to manually modify the `INPUT_FILE` in the code to point to the target `capture_list_x_x_x.json`.
> Therefore, if you modify the `output_file` in `generate_x_x_x.yaml`, please synchronously update `maprun.py`.

### 3. Configuration Instructions

#### 3.0 Prerequisites

Some configuration parameters are not directly related to the sampling process but must be manually filled in/modified to be recorded in the generated files.

> [!IMPORTANT]
> **Prerequisites**: These configuration parameters are not directly related to the sampling process, but you must manually fill them into `configs/*.yaml` before running to ensure complete metadata generation.
> Although these parameters will be mentioned again below, make sure to correctly record them in the corresponding configuration files.
>
> 1. Create a new world in Minecraft, query it using the `/seed` command, and log the seed into `generate_x_x_x.yaml`.
> 2. Set the screenshot hotkey in the Resolution Control mod, and write that key into `mod_key` in `capture_x_x_x.yaml`.
>    In the mod menu's Screenshot page, set the screenshot resolution (high resolution), note it as `hr_res`, and write it into `capture_x_x_x.yaml`.


#### 3.1 Generation Configuration (`configs/generate_x_x_x.yaml`)
- `total_samples` (int): Total number of samples, i.e., how many pairs of screenshots to capture.
- `seed` (int): Map seed, **used only for logging, must be filled manually**.
- `enable_y` (bool): Whether to output the Y-axis. When enabled, the output will include a `y` field. This option affects `enable_manual`.
- `random_y` (bool): Whether to enable random generation of Y-axis values. When enabled, the `/tp` logic is used, requiring manual entry of the desired coordinates; for unspecified coordinates or when disabled, the `/spreadplayer` logic is used. This option does not affect `enable_manual`.
- `enable_manual` (bool):
    - `true`: Read from `manual_csv_file`.
    - `false`: Auto-generate from `biomes_csv_file`.
    You only need to provide the file required for the corresponding mode.
- `biomes_csv_file` (str): Biome center input CSV (`biome,x,z`).
- `manual_csv_file` (str): Manual task input CSV (`id,biome,yaw,pitch,time,x,z[,y]`).
- `coordinate_offset` (int): Random offset radius from the center point during auto-generation (`+/-offset`).
- `yaw_range` (int_pair): Random range for yaw.
- `pitch_range` (int_pair): Random range for pitch.
- `time_points` (str): Optional time points, comma-separated.
- `output_file` (str): Output JSON path.

After `generate.py` reads the configuration, the generated JSON's `config` will log:

- `total_samples`, `enable_y`, `random_y`, `enable_manual`, `seed`, `coordinate_offset`, `yaw_range`, `pitch_range`, `time_points`
- And retains only one source field depending on the mode:
    - Manual mode: `manual_csv_file`
    - Auto mode: `biomes_csv_file`

#### 3.2 Capture Configuration (`configs/capture_x_x_x.yaml`)
- `input_file` (str): Input task JSON.
- `log_file` (str): Capture log output path and filename suffix for logs.
- `lr_res` (int_pair): Target window resolution.
- `hr_res` (int_pair): High-resolution value, **used only for logging, requires manual input in the Resolution Control Menu**.
- `wait_time` (float): Wait time before capturing each sample screenshot. Used to wait for blocks to load; can be reduced if the machine performance is good.
- `mod_key` (str): Resolution Control screenshot hotkey.
- `mc_key` (str): Minecraft screenshot hotkey.

#### 3.3 Pre-loading Configuration (`maprun.py`)

- **`INPUT_FILE`**: The input task file (e.g., `capture_list_x_x_x.json`).
- **`WAIT_TIME`**: Wait time for chunk loading.
- **`CHECK_SPREAD`**: A toggle to detect `/spreadplayers` command errors. When enabled, it monitors game logs via `MC_LOG_PATH`.
- **`MC_LOG_PATH`**: The file path to the Minecraft `latest.log`.
- **`LOG_SUFFIX`**: The output directory and file extension for the log files.

---

### 4. Data Format

#### 4.1 Biome Centers `data/biomes_x_x_x.csv`

The header order is fixed:

```csv
biome,x,z
```
*You can use some seed viewers to search for biome coordinates to make writing this file easier.*

#### 4.2 Manual Tasks `data/coords_x_x_x.csv`

When `enable_y=false`:

```csv
id,biome,yaw,pitch,time,x,z
```
When `enable_y=true`:

```csv
id,biome,yaw,pitch,time,x,z,y
```
*Manual tasks can be used for locations that are difficult to generate automatically (e.g., caves).*

#### 4.3 Task JSON

Top-level structure (Example):

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

If `enable_y=true`, each record will additionally contain a `y` field.

---

### 5. Replication Suggestions

**If you need to replicate this dataset**, please select the corresponding configuration file depending on the version and synchronize the instructed environment configuration. Using version 1.0 as an example:
```bash
# Generate capture_list_1_0_0.json manually from biomes_1_0_0.csv
python generate.py --config configs/generate_1_0_0.yaml
# (Optional, requires Minecraft to be the main window) Preload chunks
python maprun.py
# (Requires Minecraft to be the main window) Execute screenshots
python capture.py --config configs/capture_1_0_0.yaml
```
Screenshots will be saved in the screenshots folder of your Minecraft directory. Mod screenshots are prefixed with `fb`, e.g., `fb2026-03-25_19.46.17.png`, while vanilla screenshots look like `2026-03-10_15.14.38.png`. It is recommended to backup and empty this folder, and rename these "screenshot pairs" chronologically.

**If you need to create a dataset, it is recommended to**:
- Fix the `seed` to ensure random generation is reproducible.
- Keep the corresponding version configuration file (e.g., `*_1_0_0.yaml`) when publishing the dataset.
- Retain the final task JSON used for capturing, to facilitate traceability.

## About Dataset Replication

Unlike specialized rendering engines, due to the dynamic nature of the game environment, it is difficult to control variables such as Minecraft's frametime. This may cause discrepancies when attempting to reproduce events like Minecraft's animation playback or frametime-based calculations (some shaderpacks): e.g., cloud movement, raindrop effects, and lava animations.
 Since the Minecraft `/spreadplayers` command refuses to execute in unsafe locations (such as on water or lava), the script's subsequent use of `/tp` may cause players to spawn in mid-air or underground. In cases of falling into water, even with a long `WAIT_TIME`, players may remain in a falling state due to deep water, which can lead to inconsistencies between screenshots. If spawned underground, the camera view will be obstructed by blocks (a problem particularly severe in Ocean biomes). If you still require random coordinates, you should enable `enable_y` and disable `random_y`. This ensures the generated Y-coordinates are recognizable placeholder values rather than being used for teleportation. You can then manually find a safe Y-value for those stuck/floating points and update the `coords` field in the `json` file.
The method I am using combines in-game screenshots (F2) and Mod screenshots, but `pyautogui.hotkey()` cannot make these two commands function strictly simultaneously on the machine. The operational rendering pipeline itself also does not support this logic, so it is hard to maintain absolute consistency between HR and LR during actual runtime. Although this has almost no impact on static scenes (such as daytime variations), it can be quite obvious in dynamic scenes (especially raindrop effects). This introduces a certain degree of randomness for degradation models; thus, compared to using downsampling algorithms, the capture methodology itself and game characteristics make my dataset difficult to perfectly reproduce. ~~However, I believe that the random discrepancies between LR-HR pairs objectively increase the complexity of degradation model construction, enhancing the model's robustness in complex dynamic scenarios.~~

Although I used <https://github.com/UltimateBoomer/Resolution-Control> as a secondary screenshot method, I also locally modified its 1.20 branch to allow it to take a screenshot at the corresponding resolution in the frame immediately after capturing, achieving an approximate "simultaneous acquisition" effect. Tests show that this approach has no significant gap compared with this project's original solution (mixed vanilla screenshots). In detail, the falling of raindrops in Minecraft still cannot be precisely matched between the two images, which is a fundamental issue.
However, this modified version can still make your screenshots more elegant, which might suit your needs or coincide with your intentions. You can access it here: <https://github.com/Ray-Zeros/Resolution-Control>
