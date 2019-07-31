#  reading in image names
setwd("../stimuli")
image_list <- list.files()

# reading in QR code names
setwd("../QR_codes")
qr_list <- list.files()

qr_counter <- 1

# adding image names to  csv
stimuli <- data.frame(image_list)
names(stimuli) <- c("image")

#  filling top right corner with marker 1
stimuli$rightup <- rep("marker_01",nrow(stimuli))

# filling top left corner half with marker 2 and half with 3
stimuli$leftup <- rep("marker_02",nrow(stimuli))
stimuli$leftup[30:58] <- "marker_03"

# filling lower right corner - further  distinguishing with markers 4 & 5
stimuli$rightdown <- rep("marker_04", nrow(stimuli))
stimuli$rightdown[15:29] <- "marker_05"
stimuli$rightdown[44:58] <- "marker_05"

stimuli$leftdown <- rep("marker_06", nrow(stimuli))
stimuli$leftdown[] <- 