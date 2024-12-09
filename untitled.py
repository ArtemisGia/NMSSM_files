class MHiggsPlotter:
    def __init__(self, dataframe):
        self.df = dataframe

    def filter_data(self, tanb_value):
        filtered_df = dataframe[(dataframe['tanb'] == tanb_value) & (dataframe['mhiggs'].apply(lambda x: isinstance(x, list) and 
                                                                  len(x) > 0 and all(v is not None for v in x) and x[0] == min(x)))].reset_index(drop=True)
        return filtered_df

    def plot(self, tanb_value, title_suffix=""):
        valid_df, mhiggs_first, errors_first = self.filter_data(tanb_value)
        plt.figure(figsize=(8, 6))
        plt.errorbar(
            valid_df['lam'], mhiggs_first, yerr=errors_first,
            fmt='o', color='blue', ecolor='gray', capsize=5, alpha=0.7, label=f'tanb={tanb_value}'
        )
        plt.xlabel(r'$\lambda$', fontsize=14)
        plt.ylabel(r'$m_h^{(1)}$ (GeV)', fontsize=14)
        plt.title(f'Plot of $\lambda$ vs. $m_h^{(1)}$ for tanb={tanb_value} {title_suffix}', fontsize=16, weight='bold')
        plt.axhline(y=125, color='black', linestyle=':', label=r'$m_h = 125 \, \mathrm{GeV}$')
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.show()
