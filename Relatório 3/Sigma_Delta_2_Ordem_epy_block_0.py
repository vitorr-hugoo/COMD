import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Sigma-Delta 2nd Ordem",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        self.int1 = 0.0
        self.int2 = 0.0
        self.y_prev = 0.0
        self.leak = 0.999

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        for i in range(len(x)):
            error = x[i] - self.y_prev

            self.int1 = self.leak * self.int1 + 0.5 * error
            self.int2 = self.leak * self.int2 + 0.25 * self.int1

            # Anti-windup
            self.int1 = np.clip(self.int1, -1.5, 1.5)
            self.int2 = np.clip(self.int2, -1.5, 1.5)

            # Dither
            dither = 1e-4 * np.random.randn()

            y[i] = 1.0 if (self.int2 + dither) >= 0 else -1.0
            self.y_prev = y[i]

        return len(y)
