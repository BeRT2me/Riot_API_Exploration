import pandas as pd
import re
from league_lists import versions

patches = []
for i in versions:
    df = pd.read_json('http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(i))
    champs = []
    for champ in df.index:
        temp_df = pd.DataFrame.from_dict(df.loc[champ, "data"]['stats'], orient='index').reset_index().pivot(
            columns='index')
        temp_df.columns = temp_df.columns.droplevel()
        temp_df[champ] = champ
        temp_df = temp_df.groupby(champ).mean()
        champs.append(temp_df.copy())
    df = df.merge(pd.concat(champs), left_index=True, right_index=True, how='outer').drop(columns=['format', 'data'])
    patches.append(df)
base_stats = pd.concat(patches, sort=False)

base_stats.version = base_stats.version.apply(lambda x: re.search("(\d\.\d{1,2})\.", x).group(1))
base_stats.version = base_stats.version.apply(lambda x: x[:2] + '0' + x[2:] if len(x) == 3 else x)
base_stats.reset_index(inplace=True)
base_stats.rename(columns={'index': 'champion'}, inplace=True)
base_stats.attackspeed.fillna(base_stats.attackspeedoffset.apply(lambda x: round(0.625 / (1 + x), 3)), inplace=True)
ffill = base_stats[(base_stats.version == '8.23')].attackspeed.to_list()
ffill.extend(ffill)
base_stats.attackspeed.loc[base_stats.attackspeed.isnull()] = ffill
base_stats.to_pickle('all_base_stats.pkl')
