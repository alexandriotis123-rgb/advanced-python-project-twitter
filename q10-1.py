import pandas as pd
def load_data():
    ranked_df = pd.read_csv("q9_4.csv")
    return ranked_df


def find_authors_contribution(df):
   lines=len(df)
   one_perc_number_of_rows=int(lines * 0.01)
   top_authors=df[['author_id','total_bursts_participated','avg_contribution']].head(one_perc_number_of_rows).copy()
   top_authors=top_authors.rename(columns={'avg_contribution': 'avg_contribution_perc'})
   return top_authors

if __name__ == "__main__":
 ranked_df=load_data()
 top_one_perc_authors_for_contribution=find_authors_contribution(ranked_df)
 #we found the 1% of authors with the highest burst participation and the average contribution during those bursts.
 #----------q10_1 result-----------
 top_one_perc_authors_for_contribution.to_csv('q10_1.csv',index=False, float_format='%.5f')
 #----------q10_1 result-----------