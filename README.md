# Covid Data Process
## File Structure
```
.
├── 1_Gowalla
│   ├── graph_1.py
│   ├── Process_gowalla.ipynb
│   └── user_center_1.py
├── 2_Foursquare
│   ├── graph_2.py
│   ├── Process_foursquare.ipynb
│   └── user_center_2.py
├── 3_Brightkite
│   ├── 3_user_center.py
│   ├── graph_3.py
│   └── Process_Brightkite.ipynb
├── 4_HaslemereNetwork
│   ├── graph_4.py
│   └── Process_HaslemereNetwork.ipynb
├── NYC
│   ├── graph_NYC.py
│   ├── Process_NYC.ipynb
│   ├── user_center_NYC.py
│   └── user_user_distance_NYC.py
├── README.md
└── TKY
    ├── graph_TKY.py
    ├── Process_TKY.ipynb
    ├── user_center_TKY.py
    └── user_user_distance_TKY.py
```

## File Description
- `graph_{dataset_name}.py` : Generate `graph_{dataset_name}.txt`
- `user_center_{dataset_name}.py` : Generate `user_center_{dataset_name}.txt`
- `user_user_distance_{dataset_name}.py` : Generate `user_user_distance_{dataset_name}.txt`
- `Process_{dataset_name}.ipynb` : jupyter version

## .py File Location
- Put the .py file in the corresponding `{dataset_name}` folder
    - rename_folder <-> original_folder
    - `1_Gowalla` <-> `(大) Gowalla (not SNAP)`
    - `2_Foursquare` <-> `(中) Foursquare (LBSN2vec++)`
    - `3_Brightkite` <-> `(小) Brightkite`
    - `4_HaslemereNetwork` <-> `(最小) Haslemere network`
    - `NYC` <-> `dataset_tsmc2014`
    - `TKY` <-> `dataset_tsmc2014`

## Notice
- File Generate Order:
    1. `user_user_distance_{dataset_name}.py`
    2. `user_center_{dataset_name}.py`
    3. `graph_{dataset_name}.py`
