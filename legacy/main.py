import pathway as pw

print("Imported")

rdkafka_settings = {
    "bootstrap.servers": "server-address:9092",
    "security.protocol": "sasl_ssl",
    "sasl.mechanism": "SCRAM-SHA-256",
    "group.id": "$GROUP_NAME",
    "session.timeout.ms": "6000",
    "sasl.username": "username",
    "sasl.password": "********",
}


class InputSchema(pw.Schema):
    x: float
    y: float


t = pw.io.csv.read(
    "result.csv",
    schema=InputSchema,
    autocommit_duration_ms=1000,
)
pw.io.csv.write(t, "regression_input.csv")

t += t.select(
    x_square=t.x * t.x,
    x_y=t.x * t.y,
)
statistics_table = t.reduce(
    count=pw.reducers.count(),
    sum_x=pw.reducers.sum(t.x),
    sum_y=pw.reducers.sum(t.y),
    sum_x_y=pw.reducers.sum(t.x_y),
    sum_x_square=pw.reducers.sum(t.x_square),
)


def compute_a(sum_x, sum_y, sum_x_square, sum_x_y, count):
    d = count * sum_x_square - sum_x * sum_x
    if d == 0:
        return 0
    else:
        return (sum_y * sum_x_square - sum_x * sum_x_y) / d


def compute_b(sum_x, sum_y, sum_x_square, sum_x_y, count):
    d = count * sum_x_square - sum_x * sum_x
    if d == 0:
        return 0
    else:
        return (count * sum_x_y - sum_x * sum_y) / d


results_table = statistics_table.select(
    a=pw.apply(compute_a, **statistics_table),
    b=pw.apply(compute_b, **statistics_table),
)

pw.io.csv.write(results_table, "regression_output_stream.csv")

pw.run()
