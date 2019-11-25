#### IAPS: Choosing photos for SA Phase II ####
# To use, create subdirectory './IAPS/' and add tech report file 'AllSubjects_1-20.txt'
# This subdir is in the .gitignore per instructions to keep it hidden from IAPS directors

# set working directory
setwd("./SA_Stimulus/")

# Install and load packages
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
# means are both around 5

# looking at % for cutting top and bottom rated pics
(16/nrow(metrics))/2 # .67% would be top 8 pics
(14/nrow(metrics))/2 # .59% would be top 7 pics

# 5% of photos
.05*nrow(metrics) # take top 60

# checking out descriptions of photos
arrange_val <- metrics %>%
  arrange(valmn) 
unique(arrange_val$desc) # 611 levels

# filtering out some explicit topics
filtered <- arrange_val[!(arrange_val$desc == "BurnVictim" | arrange_val$desc == "Mutilation" | arrange_val$desc == "DeadBody" | arrange_val$desc == "HeadlessBody" | arrange_val$desc == "HurtDog" | arrange_val$desc == "Hanging" | arrange_val$desc == "InjuredChild" | arrange_val$desc == "InjuredDog" | arrange_val$desc == "SlicedHand"  | arrange_val$desc == "DeadMan" | arrange_val$desc == "Vomit" | arrange_val$desc == "ManOnFire" | arrange_val$desc == "BurntFace" | arrange_val$desc == "BatteredFem" | arrange_val$desc == "DeadDog" | arrange_val$desc == "DyingMan" | arrange_val$desc == "Execution" | arrange_val$desc == "BloodyKiss" | arrange_val$desc == "Suicide" | arrange_val$desc == "DeadTiger" | arrange_val$desc == "SeveredHand" | arrange_val$desc == "DeadCows" | arrange_val$desc == "BeatenFem"), ]
# check that it worked
unique(filtered$desc)

# cutting top 1% of valence photos to then visually approve of top pairs (4 pairs; .67%)
top_val =  filtered %>%
  arrange(valmn) %>%
  slice(1:60)

# cutting bottom 1% of valence photos to then visually approve of top pairs (4 pairs; .67%)
bottom_val =  filtered %>%
  arrange(desc(valmn)) %>%
  slice(1:60)
  
