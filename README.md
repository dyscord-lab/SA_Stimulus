# SA Stimulus

This repo contains the stimuli for the dyscord lab's Social Anxiety study.

## Important instructions for use

If directories `logs`, `__pycache__`, & `images` are not present:
1. Unzip all directories
2. Create directory named `logs`
3. Create directory named `__pycache__`

## File descriptions

1. `__pycache__` directory - cache directory
2. `images` directory (& `images.zip`) - images for Cyberball characters while
  tossing
3. `logs` directory - logging data from participants
4. `pictures` directory - stimuli without QR markers
5. `showpics` directory - stimuli with QR markers
6. `QR_combo.R` - script for unique pairs of QR markers for each stimulus photo
  (generates directory `showpics` using `pictures`)
7. `vbtg.py` - Intro survey, Cyberball game, stimuli presentation, outro survey

## To do

1. Update the Cyberball images (low priority)
  - If could make them somewhat larger (maybe 1.5x?), that would be great.
1. Export world timestamp at the beginning of the log
1. Start the experiment with showing a BRAND NEW QR code on the screen and
   making the participant press spacebar to make it go away. Show `reset_image`
   for 1 second after that before proceeding.
1. Update the markers to Pupil's latest version of markers (implement in
   branch first)
