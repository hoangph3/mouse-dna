# Mouse Dynamic Model

1. Format data
- Replace `Drag` state to `Move` state.
```sh
# DFL dataset
sed "s/Drag/Move/g" data/dfl/*/*.CSV -i

# Balabit dataset
sed "s/Drag/Move/g" data/balabit/training_files/*/* -i
sed "s/Drag/Move/g" data/balabit/test_files/*/* -i

# SAPImouse dataset
sed "s/Drag/Move/g" data/sapimouse/*/*.csv -i
```