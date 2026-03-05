import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Sigma-Delta 1st Ordem",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # Estados internos
        self.integrator = 0.0
        self.feedback = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        for i in range(len(x)):
            # Integra o erro
            self.integrator += x[i] - self.feedback

            # Quantizador 1-bit
            if self.integrator >= 0:
                y[i] = 1.0
            else:
                y[i] = -1.0

            # Feedback
            self.feedback = y[i]

        return len(y)
