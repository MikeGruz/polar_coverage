# R script to pull DW-nominate and Congressional data together
# for polarized Congressional sources project
# 
# 3/10/2014

# will pull Stata format from voteview site -- it's cleaner
library(foreign)
library(RCurl)

# download dw-nominate data
dw.house <- read.dta("ftp://voteview.com/junkord/HL01112D21_PRES_BSSE.DTA")
dw.senate <- read.dta("ftp://voteview.com/junkord/SL01112D21_BSSE.DTA")

# sort by icpsr id, then congress
dw.house <- dw.house[with(dw.house, order(idno, cong)),]
dw.senate <- dw.senate[with(dw.senate, order(idno, cong)),]

# loop through and create years of service variable

## house
years <- numeric(length(dw.house[,1]))
years[1] <- 0

for (i in 2:length(years)) {
  if (dw.house$idno[i] == dw.house$idno[i-1]) {
    years[i] <- years[i-1] + 1
  } else {
    years[i] <- 0
  }
}
  
dw.house$years <- years

## senate
years <- numeric(length(dw.senate[,1]))
years[1] <- 0

for (i in 2:length(years)) {
  if (dw.senate$idno[i] == dw.senate$idno[i-1]) {
    years[i] <- years[i-1] + 1
  } else {
    years[i] <- 0
  }
}

dw.senate$years <- years

rm(years)

###############
# pull in article counts from the nytimes api
# should be in folder tabdata
house.arts <- read.csv('./tabdata/house_arts.csv')
house.merged <- merge(dw.house, house.arts, by=c('idno','cong'))

# party var
house.merged$pid[house.merged$party == 100] <- "Democratic"
house.merged$pid[house.merged$party == 200] <- "Republican"

senate.merged$pid[senate.merged$party == 100] <- "Democratic"
senate.merged$pid[senate.merged$party == 200] <- "Republican"


senate.arts <- read.csv('./tabdata/senate_arts.csv')
senate.merged <- merge(dw.senate, senate.arts, by=c('idno','cong'))

# clustering standard errors
cl   <- function(dat,fm, cluster){
  require(sandwich, quietly = TRUE)
  require(lmtest, quietly = TRUE)
  M <- length(unique(cluster))
  N <- length(cluster)
  K <- fm$rank
  dfc <- (M/(M-1))*((N-1)/(N-K))
  uj  <- apply(estfun(fm),2, function(x) tapply(x, cluster, sum));
  vcovCL <- dfc*sandwich(fm, meat=crossprod(uj)/N)
  coeftest(fm, vcovCL) }








# pull Congressional info data from govtrack.us - historical and present data
# congress <- read.csv(text=getURL("https://www.govtrack.us/data/congress-legislators/legislators-historic.csv"))
# congress.cur <- read.csv(text=getURL("https://www.govtrack.us/data/congress-legislators/legislators-current.csv"))
# congress <- rbind(congress, congress.cur)
# rm(congress.cur)
# 
# #######
# # congress info prepping
# congress <- with(congress, data.frame(idno=icpsr_id,
#                                       last=last_name,
#                                       first=first_name,
#                                       birthday=birthday,
#                                       sex=gender,
#                                       state_abbr=state))
# 












