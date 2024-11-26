file = open("visit_log.csv", "r")
out = open("funnel.csv", "w")
first = True
for line in file:
    if first:
        out.write(line)
        first = False
        continue
    # only the third column matters, so don't bother splitting the entire line
    values = line.split(",", 3)
    if len(values) >= 3 and values[2] != "":
        out.write(line)
file.close()
out.close()
