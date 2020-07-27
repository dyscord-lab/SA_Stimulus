#### IAPS: Choosing photos for SA Phase II ####
#
# To use, create subdirectory './IAPS/' and add tech report
# file 'AllSubjects_1-20.txt'. This subdir is in the 
# .gitignore per instructions to keep it hidden from IAPS 
# directors
#
# By: @mchiovaro
# Last updated: 07_27_2020

# set working directory
setwd("./SA_Stimulus/")

# install and load packages
#install.packages("reader")
library(reader)
library(dplyr)

# read in metrics and cut out first few nonsense lines
metrics = n.readLines("./IAPS/AllSubjects_1-20.txt", n = 1194, skip = 6)

# convert from chr string to csv
metrics <- read.table(text = metrics)

# add in col names (manually because of weird first colname with 3 parts)
colnames(metrics) <- c("desc",	"IAPS",	"valmn",	"valsd",	"aromn",	"arosd",	"dom1mn",	"dom1sd",	"dom2mn",	"dom2sd",	"set")

# keep only what we need
metrics = metrics[,c(1, 2, 3, 5)]

# look at means for valence and arousal
mean(metrics$valmn)
mean(metrics$aromn)

# looking at % for cutting top and bottom rated pics
(15/nrow(metrics)) # 1.26% would be top 15 pics 
(30/nrow(metrics)) # 2.51% would be top 30 pics 

# identify 7% of photos so there is room for pairing
num_pics <- ceiling(.07*nrow(metrics))

# identify top 5% so most explicit photos can be filtered out
num_skip <- ceiling(.05*nrow(metrics))

# arrange by ascending valence
arrange_val <- metrics %>%
  arrange(valmn) 

# checking out descriptions of photos
unique(sort(arrange_val$desc))

# filtering out some explicit topics
filtered <- arrange_val[!(arrange_val$desc == "BurnVictim" | 
                            arrange_val$desc == "Mutilation" | 
                            arrange_val$desc == "DeadBody" | 
                            arrange_val$desc == "HeadlessBody" | 
                            arrange_val$desc == "HurtDog" | 
                            arrange_val$desc == "Hanging" | 
                            arrange_val$desc == "InjuredChild" | 
                            arrange_val$desc == "InjuredDog" | 
                            arrange_val$desc == "SlicedHand"  | 
                            arrange_val$desc == "DeadMan" | 
                            arrange_val$desc == "Vomit" | 
                            arrange_val$desc == "ManOnFire" | 
                            arrange_val$desc == "BurntFace" | 
                            arrange_val$desc == "BatteredFem" | 
                            arrange_val$desc == "DeadDog" | 
                            arrange_val$desc == "DyingMan" | 
                            arrange_val$desc == "Execution" | 
                            arrange_val$desc == "BloodyKiss" | 
                            arrange_val$desc == "Suicide" | 
                            arrange_val$desc == "DeadTiger" | 
                            arrange_val$desc == "SeveredHand" | 
                            arrange_val$desc == "DeadCows" | 
                            arrange_val$desc == "BeatenFem"), ]

# check new descriptions
unique(sort(filtered$desc))

### low valence ###

# skip top 5% of valence photos to remove explixit once, 
# then cut next 7% to keep for pairing
low_val =  filtered %>%
  arrange(valmn) %>%
  slice(num_skip:(num_skip+num_pics-1))

# take avg valence
mean(low_val$valmn)

### high valence ###
  
# cut highest 7% of valence photos to keep for pairing
high_val =  filtered %>%
  arrange(desc(valmn)) %>%
  slice(1:num_pics)

# take avg valence
mean(high_val$valmn)
