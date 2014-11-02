library(ggtern)
library(scales)
args<-commandArgs(TRUE)

name = substr(args[1], 0, nchar(args[1])-4)

dp <- read.table(paste(name, "_p.dat", sep=''), col.names = c("A", "B", "C", "E"))
elem = unlist(strsplit(name, "_"))
elem[0]
d <- read.table(paste(name, ".dat", sep =''), col.names = c("A", "B", "C", "E"))
png(paste(name, ".png", sep=''), 690, 490)
#pdf(paste(name, "_2.eps", sep=''), width=4.5, height=4, useDingbats=FALSE )
par( mai=c(0.65, 0.65, 0.1, 0.05), mgp=c(2, 0.5, 0), tck=-0.03 )

ggtern(data=data.frame(a=d$A, b=d$B, c=d$C, z=d$E),  aes(a, b, c)) +
geom_point(colour = "grey", pch=21, size=0.5) + 
stat_density2d(aes(weight=z, colour=rev(..level..)), binwidth=25) +
geom_point(data=data.frame(a1=dp$A, b1=dp$B, c1=dp$C, z1=dp$E),  aes(a1, b1, c1, colour=z1),  size=6, shape=18) +
scale_colour_gradient2(low = "blue",  high = "red", limits=c(-425, 100.0), space="Lab")+
labs(L=elem[1],T=elem[2],R=elem[3])+
theme_bw(base_size = 20) 

dev.off()
