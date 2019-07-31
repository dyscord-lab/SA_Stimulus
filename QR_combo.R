#  reading in image names
setwd("../stimuli")
image_list <- list.files()

# reading in QR code names
setwd("../QR_codes")
qr_list <- list.files()

qr_counter <- 1

stimuli <- data.frame(image_list)
names(stimuli) <- c("image")
