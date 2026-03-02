# GLB Labeler

Lightweight 3D viewer for labeling GLB files as approved/discarded.

## Usage

```bash
python3 server.py
# Open http://localhost:8080
```

## Controls

| Key | Action |
|-----|--------|
| `A` | Approve (label=1) |
| `D` | Discard (label=0) |
| `←` `→` | Navigate / edit labels |
| `S` | Save to `labels.csv` |

## Output

`labels.csv` with columns `id` (filename without .glb) and `label` (1=approved, 0=discarded).
