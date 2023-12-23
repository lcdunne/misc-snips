function randomHex(size) {
  // Create a random hex string given a specific size
  return [...Array(size)]
    .map(() => Math.floor(Math.random() * 16).toString(16))
    .join("");
}
