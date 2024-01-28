import pathway as pw
print("Imported")
table = pw.demo.range_stream()

print(table.value)


def on_change(key: pw.Pointer, row: dict, time: int, is_addition: bool):
    print(row)
    print(is_addition)
    print("Something changed")


pw.io.subscribe(table, on_change)

pw.run()
