#===========================================================================
# creating data frame for image generation
#===========================================================================

# reading in image names
setwd("./SA_Stimulus/pictures_2/stimuli")
image_list <- list.files()

# reading in QR code names
setwd("../QR_codes")
qr_list <- list.files()

# adding image names to csv
stimuli <- data.frame(image_list, stringsAsFactors = FALSE)
names(stimuli) <- c("image")

# filling top right corner with marker 1
stimuli$rightup <- rep("marker_01.png",nrow(stimuli))
stimuli$rightdown <- rep("marker_02.png",nrow(stimuli))
stimuli$leftup <- rep("marker_03.png",nrow(stimuli))
stimuli$leftdown <- rep("marker_04.png",nrow(stimuli))

#old code
# filling top left corner half with marker 2 and half with 3
#stimuli$leftup <- rep("marker_02.png",nrow(stimuli))
#stimuli$leftup[30:56] <- "marker_03.png"

# fill  ing lower right corner - further  distinguishing with markers 4 & 5
#stimuli$rightdown <- rep("marker_04.png", nrow(stimuli))
#stimuli$rightdown[15:29] <- "marker_05.png"
#stimuli$rightdown[44:56] <- "marker_05.png"

# filling lower left corner by cycling through unused markers
#stimuli$leftdown <- rep("marker_06.png", nrow(stimuli))
#stimuli$leftdown[1:14] <- qr_list[7:20]
#stimuli$leftdown[15:29] <- qr_list[7:21]
#stimuli$leftdown[30:43] <- qr_list[7:20]
#stimuli$leftdown[44:56] <- qr_list[7:19]

#===========================================================================
# creating stimuli using data frame
#===========================================================================

install.packages(c("png", "jpeg", "grid", "gridExtra", "ggplot2"))
Packages <- c("png", "jpeg", "grid", "gridExtra", "ggplot2")
lapply(Packages, library, character.only = TRUE)

# reading in blank image
blank <- readPNG('../blank.png')

setwd("../stimuli")
# loop for image generation
for (i in 1:28) {
  
  # identifying NAMES of unique QR markers
  RUname <- stimuli[i, 2]
  LUname  <- stimuli[i, 3]
  RDname <- stimuli[i, 4]
  LDname <- stimuli[i, 5]
  
  #reading in stimuli image
  imagename <- stimuli[i, 1] # also will be stimuli[i,1] in the loop
  image <- readJPEG(imagename)
  
  # creating grid image, READING the QR PNG images at the same time
  setwd("../QR_codes")
  g <- arrangeGrob(rasterGrob(readPNG(RUname)), rasterGrob(blank), rasterGrob(readPNG(LUname)),
                   rasterGrob(blank), rasterGrob(image), rasterGrob(blank),
                   rasterGrob(readPNG(RDname)), rasterGrob(blank), rasterGrob(readPNG(LDname)),
                   ncol=3, widths = c(1,15,1), heights = c(.6,2,.6))
  setwd("../")
  mypath <- "../showpics_2/"
  ggsave(file = paste0(mypath, i, ".png"), g) # "image_i.png" to have unique file names
  #dev.off()
  setwd("./stimuli/")
  
}

#### generating fixation image ####

# read in image
fixate <- readPNG('../fix_cross.png')

#
setwd("../QR_codes/")
# generate stim with QRs
g <- arrangeGrob(rasterGrob(readPNG('marker_05.png')), rasterGrob(blank), rasterGrob(readPNG('marker_06.png')),
                 rasterGrob(blank), rasterGrob(fixate), rasterGrob(blank),
                 rasterGrob(readPNG('marker_07.png')), rasterGrob(blank), rasterGrob(readPNG('marker_08.png')),
                 ncol=3, widths = c(1,15,1), heights = c(.6,2,.6))
setwd("../")
mypath <- "../showpics_2/"
ggsave(file = paste0(mypath, "fix.png"), g) 

