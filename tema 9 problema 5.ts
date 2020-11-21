// Para ejecutar este fichero: deno run fichero.ts
// @deno-types="https://raw.githubusercontent.com/pammacdotnet/FFRepo/master/mathjs.d.ts"
import math from "https://dev.jspm.io/mathjs";
import * as MathJS from "https://raw.githubusercontent.com/pammacdotnet/FFRepo/master/mathjs.d.ts";

const em: math.Unit = math.evaluate("electronMass");
const c = math.evaluate("speedOfLight");
const eenergy: math.Unit = math.multiply(
  em,
  math.pow(c, 2) as math.Unit,
);

console.log(eenergy.to("electronvolt").toString());
console.log(
  math.evaluate("1 electronMass * speedOfLight * speedOfLight to eV")
    .toString(),
);
