# MineSR: Minecraft Super-Resolution Dataset

## Overview
The MineSR dataset aims to provide paired high-resolution (1080P, acquired via mod) and low-resolution (270P, acquired via vanilla screenshots) images of Minecraft to support the training of 4x super-resolution models.

To ensure consistent degradation between training samples, we use a single rendering-scale strategy: using the Resolution Control mod to modify Buffer Size and obtain HR images.

As a Version 1.0 release, this dataset contains **1,840 pairs** of HR/LR images covering **46 different biomes**. Forty representative images were collected for each biome.

The script used to create this dataset has been open-sourced on GitHub: https://github.com/Ray-Zeros/MineSR

## Data Structure

```text
.
├── HR/                # High resolution images (1920x1080)
│   ├── 0001.png
│   └── ...
├── LR/                # Low resolution images (480x270)
│   ├── 0001.png
│   └── ...
├── metadata.csv       # Index Table (index, biome, Set Partition)
├── LICENSE            # CC BY-NC-SA 4.0
└── README.md
```

## Metadata Usage
`metadata.csv` Includes the following fields：
*   `index`: Corresponds to the filenames in the `HR/` and `LR/` folders._(e.g., '0001' for '0001.png')_
*   `biome`: Name of the Minecraft biome (46 types).
*   `split`: Official data partition:
    *   `train`: 1,472 images (80%)
    *   `val`: 184 images (10%)
    *   `test`: 184 images (10%)

## Additional Information

This dataset is released under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

**Functionality Declaration & Disclaimer:**
This project does not modify or distribute the source code of any of the aforementioned mods. Fabric API is used as the mod base library. Iris, Sodium, and Sodium Extra provide more visual and performance options. ModMenu and Reese's Sodium Options optimize UI interaction. Resolution Control is used for taking screenshots.

**Minecraft Disclaimer:**
This project is a third-party open-source tool, not associated with Mojang Studios, and is not officially endorsed by Mojang Studios. The Minecraft name, trademarks, and all related game assets are copyright of Mojang Studios. This project strictly complies with the Minecraft [End User License Agreement (EULA)](https://account.mojang.com/documents/minecraft_eula).

## Citation
If you have used this dataset in your research, please cite it in the format below, based on the **version** you used:
```bibtex
@dataset{MineSR,
  author       = {Chen, Ruixi},
  title        = {MineSR: Minecraft Super-Resolution Dataset},
  version      = {1.0},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.19294458},
  url          = {https://doi.org/10.5281/zenodo.19294458}
}
```
**APA Style:**
Chen, Ruixi (2026). MineSR: Minecraft Super-Resolution Dataset (1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19294458