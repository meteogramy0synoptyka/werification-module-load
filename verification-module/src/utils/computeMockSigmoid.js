export function computeMockSigmoid(x, slope = 0.3, intercept = 1.1) {
  return 1 / (1 + Math.exp(slope * (x + intercept)));
}
