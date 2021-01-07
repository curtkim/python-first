for NUM in 0000 0001 0002
do
  libreoffice --headless --convert-to csv HDL32-V2_Monterey\ Highway/HDL32-V2_Monterey\ Highway\ \(Frame\ $NUM\).csv.xlsx --outdir tmp
done

