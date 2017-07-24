alpha <- rnorm(100)
alpha <- sort(alpha)
alpha1 <- alpha
for (k in 1:10){
	beta <- c(1:99)
	for (i in 1:99) {
		beta[i] <- (alpha1[i] + alpha1[i+1])/2
	}
	alpha1[1] <- -((1/sqrt(2*pi))*exp((-1/2)*(beta[1])^2))/pnorm(beta[1])
	for (i in 2:99) {
		alpha1[i] <- ((1/sqrt(2*pi))*(exp((-1/2)*(beta[i])^2)-exp((-1/2)*(beta[i-1])^2)))/(pnorm(beta[i])-pnorm(beta[i-1]))
	}
	alpha1[100] <- (1/sqrt(2*pi))*exp((-1/2)*(beta[99])^2)/(1-pnorm(beta[99]))
}