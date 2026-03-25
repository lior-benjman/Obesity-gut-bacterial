if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

BiocManager::install("curatedMetagenomicData")

lechat <- curatedMetagenomicData(
  "2021-03-31.LeChatelierE_2013.relative_abundance",
  dryrun = FALSE
)

se <- lechat[[1]]

X_raw <- assay(se)
X_raw <- t(X_raw)
meta_raw <- as.data.frame(colData(se))

write.csv(X_raw, "Raw_LeChatelier_relative_abundance.csv")
write.csv(meta_raw, "Raw_LeChatelier_metadata.csv")
