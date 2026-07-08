import unittest
import pandas as pd
import numpy as np

class TestTCCDataValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Carregar datasets
        cls.df_completo = pd.read_csv("dataset_pacing_completo.csv")
        cls.df_kmeans = pd.read_csv("resultados_kmeans_todas_distancias.csv")
        
        # Recriar df_perf com keep='last' assim como no pipeline analítico
        cls.df_perf = cls.df_completo.drop_duplicates(
            subset=['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta'], 
            keep='last'
        ).copy()

    def test_final_split_integrity(self):
        """Testa se keep='last' mantém corretamente a última parcial (distancia_parcial == distancia_prova)"""
        # Para cada performance em df_perf, a distância parcial do registro deve ser igual à distância total da prova
        anomalias = self.df_perf[self.df_perf['distancia_parcial'] != self.df_perf['distancia_prova']]
        self.assertEqual(len(anomalias), 0, f"Registros em que a parcial final não bate com a distância total da prova: {anomalias[['campeonato', 'atleta', 'distancia_prova', 'distancia_parcial']].head()}")

    def test_physical_times(self):
        """Testa se os tempos finais absolutos das provas fazem sentido fisicamente para atletas de elite (sem anomalias de 3s ou 1000s)"""
        # 400m Livre de elite: tempo deve estar majoritariamente entre 3m20s (200s) e 5m30s (330s)
        df_400 = self.df_perf[self.df_perf['distancia_prova'] == 400]
        anomalias_400_baixas = df_400[df_400['tempo_acumulado_seg'] < 200]
        anomalias_400_altas = df_400[df_400['tempo_acumulado_seg'] > 360]
        self.assertLess(len(anomalias_400_baixas), 5, f"Excesso de tempos de 400m anomalamente baixos: {len(anomalias_400_baixas)}")
        self.assertLess(len(anomalias_400_altas), 5, f"Excesso de tempos de 400m anomalamente altos: {len(anomalias_400_altas)}")
        self.assertTrue(220 <= df_400['tempo_acumulado_seg'].median() <= 265, f"Mediana de 400m incorreta: {df_400['tempo_acumulado_seg'].median()}")

        # 800m Livre de elite: tempo deve estar majoritariamente entre 7m10s (430s) e 10m30s (630s)
        df_800 = self.df_perf[self.df_perf['distancia_prova'] == 800]
        anomalias_800_baixas = df_800[df_800['tempo_acumulado_seg'] < 430]
        anomalias_800_altas = df_800[df_800['tempo_acumulado_seg'] > 660]
        self.assertLess(len(anomalias_800_baixas), 5, f"Excesso de tempos de 800m anomalamente baixos: {len(anomalias_800_baixas)}")
        self.assertLess(len(anomalias_800_altas), 5, f"Excesso de tempos de 800m anomalamente altos: {len(anomalias_800_altas)}")
        self.assertTrue(450 <= df_800['tempo_acumulado_seg'].median() <= 540, f"Mediana de 800m incorreta: {df_800['tempo_acumulado_seg'].median()}")

        # 1500m Livre de elite: tempo deve estar majoritariamente entre 14m10s (850s) e 19m (1140s)
        df_1500 = self.df_perf[self.df_perf['distancia_prova'] == 1500]
        anomalias_1500_baixas = df_1500[df_1500['tempo_acumulado_seg'] < 830]
        anomalias_1500_altas = df_1500[df_1500['tempo_acumulado_seg'] > 1200]
        self.assertLess(len(anomalias_1500_baixas), 5, f"Excesso de tempos de 1500m anomalamente baixos: {len(anomalias_1500_baixas)}")
        self.assertLess(len(anomalias_1500_altas), 5, f"Excesso de tempos de 1500m anomalamente altos: {len(anomalias_1500_altas)}")
        self.assertTrue(860 <= df_1500['tempo_acumulado_seg'].median() <= 1020, f"Mediana de 1500m incorreta: {df_1500['tempo_acumulado_seg'].median()}")

    def test_relative_velocity_boundaries(self):
        """Testa se as velocidades relativas parciais estão dentro dos limites biomecânicos padrões da natação de elite (50% a 150%)"""
        # Não deve haver mais que uma quantidade residual de velocidades relativas fora de [50, 150] (por exemplo, max 50 registros)
        anomalias_vel = self.df_completo[(self.df_completo['velocidade_relativa'] < 50) | (self.df_completo['velocidade_relativa'] > 150)]
        self.assertLess(len(anomalias_vel), 50, f"Excesso de registros com velocidade relativa fora do padrão: {len(anomalias_vel)}")
        self.assertTrue(98 <= self.df_completo['velocidade_relativa'].median() <= 102, f"Mediana de velocidade relativa longe de 100%: {self.df_completo['velocidade_relativa'].median()}")

    def test_athlete_trajectory_units(self):
        """Testa se as trajetórias dos atletas no gráfico de painel 2x2 do Insight 9 estão nas unidades de minutos corretas"""
        df_l = self.df_perf.copy()
        
        # Gregorio Paltrinieri nos 1500m Livre (Piscina Longa)
        df_pal = df_l[(df_l['distancia_prova'] == 1500) & (df_l['tipo_piscina'] == 'Long Course') & (df_l['atleta'].str.contains("PALTRINIERI", na=False))].copy()
        df_pal['tempo_final_min'] = df_pal['tempo_acumulado_seg'] / 60
        self.assertTrue((df_pal['tempo_final_min'] >= 14.2).all(), "Tempo de Paltrinieri nos 1500m abaixo do fisicamente possível (< 14.2 min)!")
        self.assertTrue((df_pal['tempo_final_min'] <= 15.5).all(), "Tempo de Paltrinieri nos 1500m acima do aceitável para elite (> 15.5 min)!")

        # Katie Ledecky nos 800m Livre (Piscina Longa)
        df_led = df_l[(df_l['distancia_prova'] == 800) & (df_l['tipo_piscina'] == 'Long Course') & (df_l['atleta'].str.contains("LEDECKY", na=False))].copy()
        df_led['tempo_final_min'] = df_led['tempo_acumulado_seg'] / 60
        self.assertTrue((df_led['tempo_final_min'] >= 8.0).all(), "Tempo de Ledecky nos 800m abaixo de 8.0 min!")
        self.assertTrue((df_led['tempo_final_min'] <= 8.5).all(), "Tempo de Ledecky nos 800m acima de 8.5 min!")

        # Sun Yang nos 400m Livre (Piscina Longa)
        df_sun = df_l[(df_l['distancia_prova'] == 400) & (df_l['tipo_piscina'] == 'Long Course') & (df_l['atleta'].str.contains("SUN Yang", na=False))].copy()
        df_sun['tempo_final_min'] = df_sun['tempo_acumulado_seg'] / 60
        self.assertTrue((df_sun['tempo_final_min'] >= 3.6).all(), "Tempo de Sun Yang nos 400m abaixo de 3.6 min!")
        self.assertTrue((df_sun['tempo_final_min'] <= 3.95).all(), "Tempo de Sun Yang nos 400m acima de 3.95 min!")

if __name__ == '__main__':
    unittest.main()
