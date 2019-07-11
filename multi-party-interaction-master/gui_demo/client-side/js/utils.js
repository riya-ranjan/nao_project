function mapToObject(map) {
    const obj = {};
    for (let [key, value] of map)
        obj[key] = value;
    return obj;
}