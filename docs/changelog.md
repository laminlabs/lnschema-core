# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
:fire: Remove unncessary files | [180](https://github.com/laminlabs/lnschema-core/pull/180) | [falexwolf](https://github.com/falexwolf) | 2023-06-04 | 0.35a4
♻️ Absorb `DjangoORM.create()` in `DjangoORM.__init__()` | [178](https://github.com/laminlabs/lnschema-core/pull/178) | [falexwolf](https://github.com/falexwolf) | 2023-06-03 |
➖ Remove nbproject from code | [179](https://github.com/laminlabs/lnschema-core/pull/179) | [Koncopd](https://github.com/Koncopd) | 2023-06-03 |
🏗️ Enable Django backend | [177](https://github.com/laminlabs/lnschema-core/pull/177) | [falexwolf](https://github.com/falexwolf) | 2023-06-02 | 0.35a3
🚚 Rename lndb to lamindb-setup | [176](https://github.com/laminlabs/lnschema-core/pull/176) | [falexwolf](https://github.com/falexwolf) | 2023-06-01 | 0.35a2
🏗️ Add Django backend | [175](https://github.com/laminlabs/lnschema-core/pull/175) | [falexwolf](https://github.com/falexwolf) | 2023-05-31 | 0.35a1
👷 Refactor CI | [174](https://github.com/laminlabs/lnschema-core/pull/174) | [falexwolf](https://github.com/falexwolf) | 2023-05-30 |
🏗️ Remove SQL-level schema modules | [172](https://github.com/laminlabs/lnschema-core/pull/172) | [falexwolf](https://github.com/falexwolf) | 2023-05-25 | 0.34.0
🏗️ Introduce Django skeleton | [171](https://github.com/laminlabs/lnschema-core/pull/171) | [falexwolf](https://github.com/falexwolf) | 2023-05-24 |
♻️ Refactor types | [170](https://github.com/laminlabs/lnschema-core/pull/170) | [falexwolf](https://github.com/falexwolf) | 2023-05-23 |
♻️ Refactor `BaseORM` | [169](https://github.com/laminlabs/lnschema-core/pull/169) | [falexwolf](https://github.com/falexwolf) | 2023-05-17 | 0.33.8
🚸 Add `lazy="joined"` to some cheap joins | [168](https://github.com/laminlabs/lnschema-core/pull/168) | [falexwolf](https://github.com/falexwolf) | 2023-05-16 | 0.33.7
🎨 Replace `data` in `Features` with iterable | [167](https://github.com/laminlabs/lnschema-core/pull/167) | [sunnyosun](https://github.com/sunnyosun) | 2023-05-10 | 0.33.6
🎨 Replace `reference` with `field` in `Features` | [166](https://github.com/laminlabs/lnschema-core/pull/166) | [sunnyosun](https://github.com/sunnyosun) | 2023-05-09 | 0.33.5
✅ Use `nbproject-test` directly | [165](https://github.com/laminlabs/lnschema-core/pull/165) | [Koncopd](https://github.com/Koncopd) | 2023-05-04 |
✨ Enable `.lookup()` | [164](https://github.com/laminlabs/lnschema-core/pull/164) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-24 | 0.33.4
🎨 Refactor `ln.File` | [163](https://github.com/laminlabs/lnschema-core/pull/163) | [falexwolf](https://github.com/falexwolf) | 2023-04-24 | 0.33.3
⚡️ Do not change key for in-memory data replace | [162](https://github.com/laminlabs/lnschema-core/pull/162) | [Koncopd](https://github.com/Koncopd) | 2023-04-23 | 0.33.2
✨ Change File.replace handling of key | [161](https://github.com/laminlabs/lnschema-core/pull/161) | [Koncopd](https://github.com/Koncopd) | 2023-04-23 |
🚚 Move `Folder.subset` to lamindb | [160](https://github.com/laminlabs/lnschema-core/pull/160) | [falexwolf](https://github.com/falexwolf) | 2023-04-22 |
🐛 Fix population of `transform_id` in `File` in edge cases | [159](https://github.com/laminlabs/lnschema-core/pull/159) | [falexwolf](https://github.com/falexwolf) | 2023-04-21 | 0.33.1
🚚 Better names, more relationships directly on `File` | [157](https://github.com/laminlabs/lnschema-core/pull/157) | [falexwolf](https://github.com/falexwolf) | 2023-04-16 | 0.33.0
🐛 Fix `.replace()` for key != None | [156](https://github.com/laminlabs/lnschema-core/pull/156) | [falexwolf](https://github.com/falexwolf) | 2023-04-13 | 0.32.2
🎨 Set `Transform` id upon insert, update `Transform` default | [154](https://github.com/laminlabs/lnschema-core/pull/154) | [falexwolf](https://github.com/falexwolf) | 2023-04-12 | 0.32.1
🚚 Add app type | [155](https://github.com/laminlabs/lnschema-core/pull/155) | [falexwolf](https://github.com/falexwolf) | 2023-04-12 |
🩹 Fix name check in replace | [153](https://github.com/laminlabs/lnschema-core/pull/153) | [Koncopd](https://github.com/Koncopd) | 2023-04-10 |
✨ Overwrite key in replace if needed | [152](https://github.com/laminlabs/lnschema-core/pull/152) | [Koncopd](https://github.com/Koncopd) | 2023-04-10 |
🚸 Use full filename to populate `File.name`, introduce `File.key` and `Folder.key` | [150](https://github.com/laminlabs/lnschema-core/pull/150) | [falexwolf](https://github.com/falexwolf) | 2023-04-08 | 0.32.0
✨ Add `File.replace()` and `File.stage()` | [149](https://github.com/laminlabs/lnschema-core/pull/149) | [Koncopd](https://github.com/Koncopd) | 2023-04-03 | 0.31.0
♻️ Refactor ORM defintions | [148](https://github.com/laminlabs/lnschema-core/pull/148) | [falexwolf](https://github.com/falexwolf) | 2023-03-29 | 0.30.0
🚚 Add `reference` to `Transform` | [147](https://github.com/laminlabs/lnschema-core/pull/147) | [falexwolf](https://github.com/falexwolf) | 2023-03-25 | 0.30rc5
💚 Add weak backward compat | [commit](https://github.com/laminlabs/lnschema-core/commit/aa5ce2c272f0d9f14d7fa36a1298705c8ae6dda2) | [falexwolf](https://github.com/falexwolf) | 2023-03-24 | 0.30rc4
🚚 Rename `DObject` to `File` and `DFolder` to `Folder` | [146](https://github.com/laminlabs/lnschema-core/pull/146) | [falexwolf](https://github.com/falexwolf) | 2023-03-24 | 0.30rc3
🎨 Simplify `Run` | [145](https://github.com/laminlabs/lnschema-core/pull/145) | [falexwolf](https://github.com/falexwolf) | 2023-03-23 |
🏗️ Combine `Notebook` and `Pipeline` into `Transform` | [144](https://github.com/laminlabs/lnschema-core/pull/144) | [falexwolf](https://github.com/falexwolf) | 2023-03-23 | 0.30rc2
🔥 Remove Usage ORM | [143](https://github.com/laminlabs/lnschema-core/pull/143) | [falexwolf](https://github.com/falexwolf) | 2023-03-22 | 0.30rc1
⬆️ typeguard<3.0.0 and update lamindb | [141](https://github.com/laminlabs/lnschema-core/pull/141) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-15 | 0.29.7
🚑 Fix __name__ of reltype | [137](https://github.com/laminlabs/lnschema-core/pull/137) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.6
📝 Fix docs reference | [commit](https://github.com/laminlabs/lnschema-core/commit/e5b7d5d0bc7180e7c145f5ad7eac75db5928fde5) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.5
🚸 Be smart about `global_context` and `load_latest` | [136](https://github.com/laminlabs/lnschema-core/pull/136) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.4
🚚 Rename ref to reference, added backward compat for features_ref | [135](https://github.com/laminlabs/lnschema-core/pull/135) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-14 | 0.29.3
✨ Implement ln.Features | [134](https://github.com/laminlabs/lnschema-core/pull/134) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-14 | 0.29.3rc1
🚚 Move track_run logic here | [133](https://github.com/laminlabs/lnschema-core/pull/133) | [falexwolf](https://github.com/falexwolf) | 2023-03-13 | 0.29.2
🚚 Rename get_object to get | [132](https://github.com/laminlabs/lnschema-core/pull/132) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-01 | 0.29.1
📝 Fix docs references | [130](https://github.com/laminlabs/lnschema-core/pull/130) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 | 0.29.0
📝 Use lamin instead of lndb in guides | [129](https://github.com/laminlabs/lnschema-core/pull/129) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
👷 Minimal docs build | [128](https://github.com/laminlabs/lnschema-core/pull/128) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
🚸 Change user id back to base62 | [127](https://github.com/laminlabs/lnschema-core/pull/127) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
✨ Added `get_dobject` to DFolder | [126](https://github.com/laminlabs/lnschema-core/pull/126) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-24 | 0.28.7
✨ Added unique constraint uq_storage__objectkey_suffix | [125](https://github.com/laminlabs/lnschema-core/pull/125) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-24 |
👷 Use `laminci` | [124](https://github.com/laminlabs/lnschema-core/pull/124) | [falexwolf](https://github.com/falexwolf) | 2023-02-23 |
✨ Create helper functions to add relationships | [121](https://github.com/laminlabs/lnschema-core/pull/121) | [bpenteado](https://github.com/bpenteado) | 2023-02-23 | 0.28.6
✏️ Fixed folderkey typo | [123](https://github.com/laminlabs/lnschema-core/pull/123) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.5
🐛 Fixed getting objectkey | [122](https://github.com/laminlabs/lnschema-core/pull/122) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.4
🚚 Rename dobjects_features to dobject_features | [120](https://github.com/laminlabs/lnschema-core/pull/120) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.3
🚚 Rename _filekey and _folderkey to _objectkey | [119](https://github.com/laminlabs/lnschema-core/pull/119) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.2
👷 Upload run outputs to `lamin-site-assets` | [116](https://github.com/laminlabs/lnschema-core/pull/116) | [falexwolf](https://github.com/falexwolf) | 2023-02-22 |
✨ Create DFolder from a folder | [113](https://github.com/laminlabs/lnschema-core/pull/113) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-22 | 0.28.1
🚚 Rename `DObject.run_id` to `DObject.source_id` | [114](https://github.com/laminlabs/lnschema-core/pull/114) | [falexwolf](https://github.com/falexwolf) | 2023-02-21 | 0.28.0
🚑 Fix determination of postgres vs sqlite | [112](https://github.com/laminlabs/lnschema-core/pull/112) | [falexwolf](https://github.com/falexwolf) | 2023-02-17 |
✨ Add relationship between `DFolder` and `DObject` | [110](https://github.com/laminlabs/lnschema-core/pull/110) | [bpenteado](https://github.com/bpenteado) | 2023-02-16 | 0.27.1
🚚 Add column `external_id` to `Run` | [109](https://github.com/laminlabs/lnschema-core/pull/109) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 | 0.27.0
🔧 Ensure all id lengths are multiples of 4 | [108](https://github.com/laminlabs/lnschema-core/pull/108) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 |
🚚 Move `storage` table back to `core` module | [89](https://github.com/laminlabs/lnschema-core/pull/89) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 | 0.26.1
🔥 Remove migration files | [107](https://github.com/laminlabs/lnschema-core/pull/107) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-14 | 0.26.0
⬆️ Upgrade and rename `lndb_setup` to `lndb` (v0.32.0) | [105](https://github.com/laminlabs/lnschema-core/pull/105) | [bpenteado](https://github.com/bpenteado) | 2023-02-13 | 0.25.12
🚚 Rename `track_runin` to `is_run_input` | [104](https://github.com/laminlabs/lnschema-core/pull/104) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-13 | 0.25.11
✨ Added track_runin to DObject.load() | [103](https://github.com/laminlabs/lnschema-core/pull/103) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-13 | 0.25.10
💄 Fix ORM preview message | [102](https://github.com/laminlabs/lnschema-core/pull/102) | [bpenteado](https://github.com/bpenteado) | 2023-02-07 |
🚸 Introduce ORM relationship previews | [101](https://github.com/laminlabs/lnschema-core/pull/101) | [bpenteado](https://github.com/bpenteado) | 2023-02-07 |
🚚 Rename `DSet` to `DFolder` | [100](https://github.com/laminlabs/lnschema-core/pull/100) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-07 | 0.25.9
🔥  Disable ORM relationship preview | [99](https://github.com/laminlabs/lnschema-core/pull/99) | [bpenteado](https://github.com/bpenteado) | 2023-02-02 | 0.25.8
🐛 Fix assigning _cloud_filepath | [98](https://github.com/laminlabs/lnschema-core/pull/98) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.7
✨ Added _filekey to DObject for custom file keys | [97](https://github.com/laminlabs/lnschema-core/pull/97) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.6
✨ Added _cloud_filepath private attribute | [96](https://github.com/laminlabs/lnschema-core/pull/96) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.5
✨ Add rich string representation for ORM classes | [95](https://github.com/laminlabs/lnschema-core/pull/95) | [bpenteado](https://github.com/bpenteado) | 2023-01-31 | 0.25.4
🚸 Auto populate fk constrained fields from `Relationship`s | [94](https://github.com/laminlabs/lnschema-core/pull/94) | [bpenteado](https://github.com/bpenteado) | 2023-01-26 | 0.25.3
🐛 Fix strict type checking for relationships | [93](https://github.com/laminlabs/lnschema-core/pull/93) | [bpenteado](https://github.com/bpenteado) | 2023-01-24 | 0.25.2
🩹 Fix error message in `Relationship` type checking | [92](https://github.com/laminlabs/lnschema-core/pull/92) | [bpenteado](https://github.com/bpenteado) | 2023-01-23 | 0.25.1
✨ Enable data validation with pydantic | [91](https://github.com/laminlabs/lnschema-core/pull/91) | [bpenteado](https://github.com/bpenteado) | 2023-01-20 | 0.25.0
🩹 Fix `_dbconfig` | [90](https://github.com/laminlabs/lnschema-core/pull/90) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.24.1
👷 Extend CI to py3.8-3.10 | [88](https://github.com/laminlabs/lnschema-core/pull/88) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-12 |
🚚 Add `title` field to `Notebook` | [87](https://github.com/laminlabs/lnschema-core/pull/87) | [falexwolf](https://github.com/falexwolf) | 2023-01-09 | 0.24.0
🔥 Remove backward compat | [86](https://github.com/laminlabs/lnschema-core/pull/86) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
👷 Reformat to 176 char line length | [85](https://github.com/laminlabs/lnschema-core/pull/85) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
🐛 Fixed bug in DObject not autogenerate id | [84](https://github.com/laminlabs/lnschema-core/pull/84) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-14 | 0.23.2
📝 Update docstring | [83](https://github.com/laminlabs/lnschema-core/pull/83) | [falexwolf](https://github.com/falexwolf) | 2022-12-12 |
🚚 Rename input to inputs | [81](https://github.com/laminlabs/lnschema-core/pull/81) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.23.1
🐛 Avoid double construction | [80](https://github.com/laminlabs/lnschema-core/pull/80) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.23.0
🐛 Fix privates | [79](https://github.com/laminlabs/lnschema-core/pull/79) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.22.4
🐛 Fix size | [78](https://github.com/laminlabs/lnschema-core/pull/78) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.22.3
✨ Combine `record` with `DObject` | [77](https://github.com/laminlabs/lnschema-core/pull/77) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-09 | 0.22.2
🥅 Fully module-qualified path for `Pipeline` | [75](https://github.com/laminlabs/lnschema-core/pull/75) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 |
💄 Prettify noxfile | [74](https://github.com/laminlabs/lnschema-core/pull/74) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 |
♻️ Clean up migration tests | [73](https://github.com/laminlabs/lnschema-core/pull/73) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 | 0.22.1
✅ Migration testing primitives on postgres | [72](https://github.com/laminlabs/lnschema-core/pull/72) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 |
🚚 Rename `Jupynb` to `Notebook` and add relationships | [69](https://github.com/laminlabs/lnschema-core/pull/69) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 | 0.22.0
🎨 Reorganize, more tests, change `size` to BigInt | [68](https://github.com/laminlabs/lnschema-core/pull/68) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 |
✨ `add_relationship_keys` function | [67](https://github.com/laminlabs/lnschema-core/pull/67) | [falexwolf](https://github.com/falexwolf) | 2022-12-06 |
🐛 Fix import | [66](https://github.com/laminlabs/lnschema-core/pull/66) | [falexwolf](https://github.com/falexwolf) | 2022-12-05 | 0.21.2
✨ Bypass load settings | [65](https://github.com/laminlabs/lnschema-core/pull/65) | [fredericenard](https://github.com/fredericenard) | 2022-12-02 |
🎨 Prettify API & docs | [64](https://github.com/laminlabs/lnschema-core/pull/64) | [falexwolf](https://github.com/falexwolf) | 2022-11-28 |
🍱 Add tested migration | [63](https://github.com/laminlabs/lnschema-core/pull/63) | [falexwolf](https://github.com/falexwolf) | 2022-11-28 | 0.21.1
🚚 Move storage to public | [62](https://github.com/laminlabs/lnschema-core/pull/62) | [fredericenard](https://github.com/fredericenard) | 2022-11-24 | 0.21.0
🚚 Rename `checksum` to `hash` | [60](https://github.com/laminlabs/lnschema-core/pull/60) | [falexwolf](https://github.com/falexwolf) | 2022-11-18 | 0.20.0
🏗️ Add `Features` table | [59](https://github.com/laminlabs/lnschema-core/pull/59) | [falexwolf](https://github.com/falexwolf) | 2022-11-17 | 0.19.0
✨ Add `path` property to `DObject` | [58](https://github.com/laminlabs/lnschema-core/pull/58) | [falexwolf](https://github.com/falexwolf) | 2022-11-14 | 0.18.0
💚 Fix migration | [57](https://github.com/laminlabs/lnschema-core/pull/57) | [falexwolf](https://github.com/falexwolf) | 2022-11-12 | 0.17.1
🏗️ Aggregate `Run` and `DTransform` | [56](https://github.com/laminlabs/lnschema-core/pull/56) | [falexwolf](https://github.com/falexwolf) | 2022-11-11 | 0.17.0
🍱 Add migration for postgres | [55](https://github.com/laminlabs/lnschema-core/pull/55) | [falexwolf](https://github.com/falexwolf) | 2022-11-10 | 0.16.1
🚚 Rename `PipeineRun` to `Run` | [54](https://github.com/laminlabs/lnschema-core/pull/54) | [falexwolf](https://github.com/falexwolf) | 2022-11-10 | 0.16.0
🐛 Fix prefix II | [53](https://github.com/laminlabs/lnschema-core/pull/53) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.15.2
🐛 Fix prefix | [52](https://github.com/laminlabs/lnschema-core/pull/52) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.15.1
🎨 Camel case class names | [51](https://github.com/laminlabs/lnschema-core/pull/51) | [falexwolf](https://github.com/falexwolf) | 2022-11-02 | 0.15.0
🍱 Migration and fixes for postgres | [50](https://github.com/laminlabs/lnschema-core/pull/50) | [falexwolf](https://github.com/falexwolf) | 2022-11-02 |
✨ Schema modules on SQL level | [49](https://github.com/laminlabs/lnschema-core/pull/49) | [falexwolf](https://github.com/falexwolf) | 2022-11-01 |
🧑‍💻 Added naming convention | [47](https://github.com/laminlabs/lnschema-core/pull/47) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-20 |
✨ Added `dset` and `project` | [46](https://github.com/laminlabs/lnschema-core/pull/46) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-19 | 0.14.0
🚚 Rename query to select | [45](https://github.com/laminlabs/lnschema-core/pull/45) | [falexwolf](https://github.com/falexwolf) | 2022-10-12 | 0.13.0
🐛 Add migration version | - | [falexwolf](https://github.com/falexwolf) | 2022-10-11 | 0.12.1
✨ Add `checksum` column | [43](https://github.com/laminlabs/lnschema-core/pull/43) | [fredericenard](https://github.com/fredericenard) | 2022-10-11 | 0.12.0
🚚 Add `name` column to user | [42](https://github.com/laminlabs/lnschema-core/pull/42) | [falexwolf](https://github.com/falexwolf) | 2022-10-10 | 0.11.0
🩹 Fix migration script | [41](https://github.com/laminlabs/lnschema-core/pull/41) | [falexwolf](https://github.com/falexwolf) | 2022-10-07 | 0.10.1
🚸 Auto-populated CreatedBy | [40](https://github.com/laminlabs/lnschema-core/pull/40) | [falexwolf](https://github.com/falexwolf) | 2022-10-07 | 0.10.0
🏗️ Remove version column from dobject | [39](https://github.com/laminlabs/lnschema-core/pull/39) | [falexwolf](https://github.com/falexwolf) | 2022-09-30 | 0.9.0
👷 Fix CI setup | [37](https://github.com/laminlabs/lnschema-core/pull/37) | [falexwolf](https://github.com/falexwolf) | 2022-09-26 |
🚸 Fix type annotations of primary keys and add docstrings everywhere  | [35](https://github.com/laminlabs/lnschema-core/pull/35) | [falexwolf](https://github.com/falexwolf) | 2022-09-26 | 0.8.1
✨ Add `size` field to `dobject` | [32](https://github.com/laminlabs/lnschema-core/pull/32) | [falexwolf](https://github.com/falexwolf) | 2022-09-25 | 0.8.0
🍱 Add migration script | [34](https://github.com/laminlabs/lnschema-core/pull/34) | [falexwolf](https://github.com/falexwolf) | 2022-09-24 | 0.7.3
🩹 Fix type annotation of timestamps | [33](https://github.com/laminlabs/lnschema-core/pull/33) | [falexwolf](https://github.com/falexwolf) | 2022-09-24 |
💄 Add noqa to script mako & simpler unique constraint | [31](https://github.com/laminlabs/lnschema-core/pull/31) | [falexwolf](https://github.com/falexwolf) | 2022-09-23 |
✨ Add `insert` to `type.usage` | [30](https://github.com/laminlabs/lnschema-core/pull/30) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-21 |
🚚 Move migrations to package | [29](https://github.com/laminlabs/lnschema-core/pull/29) | [falexwolf](https://github.com/falexwolf) | 2022-09-20 | 0.7.2
🚚 Rename `file_suffix` to `suffix` | [28](https://github.com/laminlabs/lnschema-core/pull/28) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 | 0.7.1
✨ Rename time stamps and make them server default | [27](https://github.com/laminlabs/lnschema-core/pull/27) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 | 0.7.0
🚚 Move testdb into tests dir | [26](https://github.com/laminlabs/lnschema-core/pull/26) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 |
✨ Enable independent migrations across modules | [25](https://github.com/laminlabs/lnschema-core/pull/25) | [falexwolf](https://github.com/falexwolf) | 2022-09-15 | 0.6.0
🩹 Add timestamps to `pipeline` | [24](https://github.com/laminlabs/lnschema-core/pull/24) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 | 0.5.1
🐛 Re-export `pipeline` at root level | [23](https://github.com/laminlabs/lnschema-core/pull/23) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 |
✨ Add table `pipeline` | [22](https://github.com/laminlabs/lnschema-core/pull/22) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 | 0.5.0
♻️ Refactor id, create `type` submodule | [21](https://github.com/laminlabs/lnschema-core/pull/21) | [falexwolf](https://github.com/falexwolf) | 2022-08-24 |
🚸 Change instance & storage id to 10 char, overhaul ID module | [20](https://github.com/laminlabs/lnschema-core/pull/20) | [falexwolf](https://github.com/falexwolf) | 2022-08-24 |
Use id to reference storage | [19](https://github.com/laminlabs/lnschema-core/pull/19) | [fredericenard](https://github.com/fredericenard) | 2022-08-23 | 0.4.1
🚚 Add migration for v0.4.0 | [16](https://github.com/laminlabs/lnschema-core/pull/16) | [falexwolf](https://github.com/falexwolf) | 2022-08-22 | 0.4.0
🏗️ Add indexes and remove `dtransform_out` | [15](https://github.com/laminlabs/lnschema-core/pull/15) | [falexwolf](https://github.com/falexwolf) | 2022-08-22 |
🏗️ Track cloud workspace location | [14](https://github.com/laminlabs/lnschema-core/pull/14) | [fredericenard](https://github.com/fredericenard) | 2022-08-20 | 0.3.3
🚚 Rename package from `lndb-schema-core` to `lnschema-core` | [10](https://github.com/laminlabs/lnschema-core/pull/10) | [falexwolf](https://github.com/falexwolf) | 2022-08-19 | 0.3.2
🗃️ Rename `pipeline` to `pipeline_run` and remove `v` | [9](https://github.com/laminlabs/lnschema-core/pull/9) | [bpenteado](https://github.com/bpenteado) | 2022-08-18 | 0.3.1
🚚 Add migration from v0.1.1 to v0.3.0 | [8](https://github.com/laminlabs/lnschema-core/pull/8) | [falexwolf](https://github.com/falexwolf) | 2022-08-08 |
🚚 Rename `track_do` to `usage` | [6](https://github.com/laminlabs/lnschema-core/pull/6) | [falexwolf](https://github.com/falexwolf) | 2022-08-03 | 0.3.0
🏗️ Attach id `yvzi` and add version table `version_yvzi` | [5](https://github.com/laminlabs/lnschema-core/pull/5) | [falexwolf](https://github.com/falexwolf) | 2022-08-03 |
🗃️ Add `user.handle` | [4](https://github.com/laminlabs/lnschema-core/pull/4) | [falexwolf](https://github.com/falexwolf) | 2022-08-01 | 0.2.1
🏗️ Schema v0.2.0 with `dtransform` | [3](https://github.com/laminlabs/lnschema-core/pull/3) | [falexwolf](https://github.com/falexwolf) | 2022-07-29 | 0.2.0
🚚 Add migrations from `lamindb-schema` | [2](https://github.com/laminlabs/lnschema-core/pull/2) | [falexwolf](https://github.com/falexwolf) | 2022-07-28 |
🚚 Move code from `lamindb-schema` | [1](https://github.com/laminlabs/lnschema-core/pull/1) | [falexwolf](https://github.com/falexwolf) | 2022-07-23 | 0.1.0
