#===========================================================================
# creating data frame for image generation
#===========================================================================

# reading in image names
setwd("../stimuli")
image_list <- list.files()

# reading in QR code names
setwd("../QR_codes")
qr_list <- list.files()

# adding image names to  csv
stimuli <- data.frame(image_list)
names(stimuli) <- c("image")

# filling top right corner with marker 1
stimuli$rightup <- rep("marker_01.png",nrow(stimuli))

# filling top left corner half with marker 2 and half with 3
stimuli$leftup <- rep("marker_02.png",nrow(stimuli))
stimuli$leftup[30:58] <- "marker_03.png"

# filling lower right corner - further  distinguishing with markers 4 & 5
stimuli$rightdown <- rep("marker_04.png", nrow(stimuli))
stimuli$rightdown[15:29] <- "marker_05.png"
stimuli$rightdown[44:58] <- "marker_05.png"

# filling lower left corner by cycling through unused markers
stimuli$leftdown <- rep("marker_06.png", nrow(stimuli))
stimuli$leftdown[1:14] <- qr_list[7:20]
stimuli$leftdown[15:29] <- qr_list[7:21]
stimuli$leftdown[30:43] <- qr_list[7:20]
stimuli$leftdown[44:58] <- qr_list[7:21]

#===========================================================================
# creating stimuli using data frame
#===========================================================================

install.packages(c("png", "jpeg", "grid", "gridExtra"))
Packages <- c("png", "jpeg", "grid", "gridExtra")
lapply(Packages, library, character.only = TRUE)

##### just testing the image reading
setwd("..")
mark <- readPNG('./pictures/QR_codes/marker_01.png')
pic <- readJPEG('./pictures/stimuli/01_01.jpg')
####

#for (i in 1:58){
# }

RUname <- stimuli[1, 2]
LUname  <- stimuli[1, 3]
RDname <- stimuli[1, 4]
LDname <- stimuli[1, 5]
blank <- readPNG('./pictures/blank.png')

setwd("./pictures/QR_codes")

png(file = "../test.png", width = 10, height = 10, units = "in", res = 300)
grid.arrange(rasterGrob(readPNG(RUname)), rasterGrob(blank), rasterGrob(readPNG(LUname)), rasterGrob(blank), rasterGrob(blank), rasterGrob(blank), rasterGrob(readPNG(RDname)), rasterGrob(blank), rasterGrob(readPNG(LDname)), ncol=3 )
dev.off()


