import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Green AI Data Story",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Charge et nettoie les données du fichier CSV"""
    try:
        # Chargement du fichier CSV
        df = pd.read_csv('green Ai - Unpivoted (1).csv')
        
        # Transformation du format comparaison vers format standard
        # Créer deux DataFrames séparés pour les modèles A et B
        df_a = df[['question_id', 'question_categorie', 'categorie_model', 'model A', 'token A', 
                   'time A (sec)', 'score A', 'cost A (€)', 'electricity A (wh)', 'co2 A (g)']].copy()
        df_b = df[['question_id', 'question_categorie', 'categorie_model', 'model B', 'token B', 
                   'time B (sec)', 'score B', 'cost B (€)', 'electricity B (wh)', 'co2 B (g)']].copy()
        
        # Renommer les colonnes pour avoir un format uniforme
        df_a.columns = ['question_id', 'question_categorie', 'categorie_model', 'model', 'tokens', 
                        'time (sec)', 'score', 'cost (€)', 'electricity (wh)', 'co2 (g)']
        df_b.columns = ['question_id', 'question_categorie', 'categorie_model', 'model', 'tokens', 
                        'time (sec)', 'score', 'cost (€)', 'electricity (wh)', 'co2 (g)']
        
        # Ajouter une colonne pour identifier le modèle (A ou B)
        df_a['model_position'] = 'A'
        df_b['model_position'] = 'B'
        
        # Combiner les deux DataFrames
        df_combined = pd.concat([df_a, df_b], ignore_index=True)
        
        # Nettoyage des données
        numeric_columns = ['tokens', 'time (sec)', 'score', 'electricity (wh)', 'co2 (g)']
        
        for col in numeric_columns:
            if col in df_combined.columns:
                # Remplacer les virgules par des points et convertir en numérique
                df_combined[col] = df_combined[col].astype(str).str.replace(',', '.').replace('', np.nan)
                df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')
        
        # Supprimer les lignes avec des valeurs manquantes critiques
        df_combined = df_combined.dropna(subset=['model', 'categorie_model'])
        
        # Pour les tokens, remplacer les NaN par la médiane de chaque modèle
        df_combined['tokens'] = df_combined.groupby('model')['tokens'].transform(lambda x: x.fillna(x.median()))
        
        # Si encore des NaN dans tokens, utiliser la médiane globale
        if df_combined['tokens'].isna().any():
            df_combined['tokens'] = df_combined['tokens'].fillna(df_combined['tokens'].median())
        
        # S'assurer qu'il n'y a pas de valeurs négatives ou nulles pour size
        df_combined['tokens'] = df_combined['tokens'].clip(lower=1)
        
        return df_combined
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

def main():
    # Titre principal
    st.markdown('<h1 class="main-header">🌱 Green AI Data Story</h1>', unsafe_allow_html=True)
    st.markdown("### Analyse comparative des modèles d'IA : Performance vs Impact Environnemental")
    
    # Chargement des données
    df = load_data()
    
    if df is None:
        st.error("Impossible de charger les données. Vérifiez que le fichier CSV est présent.")
        return
    
    # Sidebar pour les filtres
    st.sidebar.header("🔧 Filtres")
    
    # Filtre par catégorie de question
    question_categories = st.sidebar.multiselect(
        "Catégories de questions:",
        options=df['question_categorie'].unique(),
        default=df['question_categorie'].unique()
    )
    
    # Filtre par catégorie de modèle
    categories = st.sidebar.multiselect(
        "Catégories de modèles:",
        options=df['categorie_model'].unique(),
        default=df['categorie_model'].unique()
    )
    
    # Filtre par modèle
    models = st.sidebar.multiselect(
        "Modèles spécifiques:",
        options=df['model'].unique(),
        default=df['model'].unique()
    )
    
    # Filtre par score minimum
    min_score = st.sidebar.slider(
        "Score minimum:",
        min_value=0,
        max_value=5,
        value=0,
        step=1
    )
    
    # Application des filtres
    filtered_df = df[
        (df['question_categorie'].isin(question_categories)) &
        (df['categorie_model'].isin(categories)) &
        (df['model'].isin(models)) &
        (df['score'] >= min_score)
    ]
    
    # Métriques globales
    st.header("📊 Vue d'ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_models = filtered_df['model'].nunique()
        st.metric("Nombre de modèles", total_models)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_score = filtered_df['score'].mean()
        st.metric("Score moyen", f"{avg_score:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_electricity = filtered_df['electricity (wh)'].sum()
        st.metric("Consommation totale", f"{total_electricity:.1f} Wh")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_co2 = filtered_df['co2 (g)'].sum()
        st.metric("Émissions CO₂", f"{total_co2:.1f} g")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Analyse par Catégorie de Modèle", 
        "⚖️ Comparaison entre Catégories", 
        "🏆 Comparaison Générale des Modèles",
        "❓ Analyse par Type de Question"
    ])
    
    # ===== SECTION 1: ANALYSE PAR CATÉGORIE DE MODÈLE =====
    with tab1:
        st.header("🔍 Analyse Détaillée par Catégorie de Modèle")
        
        # Sélection de la catégorie à analyser
        selected_category = st.selectbox(
            "Choisissez une catégorie de modèle à analyser:",
            options=filtered_df['categorie_model'].unique()
        )
        
        category_data = filtered_df[filtered_df['categorie_model'] == selected_category]
        
        if not category_data.empty:
            # Métriques pour la catégorie sélectionnée
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Modèles dans cette catégorie", category_data['model'].nunique())
            with col2:
                st.metric("Score moyen", f"{category_data['score'].mean():.2f}")
            with col3:
                st.metric("CO₂ moyen", f"{category_data['co2 (g)'].mean():.2f}g")
            with col4:
                st.metric("Temps moyen", f"{category_data['time (sec)'].mean():.2f}s")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance par modèle dans cette catégorie
                model_perf = category_data.groupby('model').agg({
                    'score': 'mean',
                    'time (sec)': 'mean'
                }).round(2)
                
                fig_model_score = px.bar(
                    x=model_perf.index,
                    y=model_perf['score'],
                    title=f"Score Moyen - Catégorie {selected_category}",
                    labels={'x': 'Modèle', 'y': 'Score moyen'},
                    color=model_perf['score'],
                    color_continuous_scale='Viridis'
                )
                fig_model_score.update_layout(height=400)
                st.plotly_chart(fig_model_score, use_container_width=True)
                
                # Impact environnemental par modèle
                model_env = category_data.groupby('model').agg({
                    'co2 (g)': 'mean',
                    'electricity (wh)': 'mean'
                }).round(2)
                
                fig_model_co2 = px.bar(
                    x=model_env.index,
                    y=model_env['co2 (g)'],
                    title=f"Émissions CO₂ - Catégorie {selected_category}",
                    labels={'x': 'Modèle', 'y': 'CO₂ moyen (g)'},
                    color=model_env['co2 (g)'],
                    color_continuous_scale='Reds'
                )
                fig_model_co2.update_layout(height=400)
                st.plotly_chart(fig_model_co2, use_container_width=True)
            
            with col2:
                # Distribution des scores dans cette catégorie
                fig_dist_score = px.histogram(
                    category_data,
                    x='score',
                    color='model',
                    title=f"Distribution des Scores - Catégorie {selected_category}",
                    nbins=10
                )
                fig_dist_score.update_layout(height=400)
                st.plotly_chart(fig_dist_score, use_container_width=True)
                
                # Corrélation temps vs performance pour cette catégorie
                plot_data_cat = category_data.dropna(subset=['time (sec)', 'score', 'tokens'])
                
                fig_time_score_cat = px.scatter(
                    plot_data_cat,
                    x='time (sec)',
                    y='score',
                    color='model',
                    size='tokens',
                    title=f"Temps vs Score - Catégorie {selected_category}",
                    labels={'time (sec)': 'Temps (sec)', 'score': 'Score'}
                )
                fig_time_score_cat.update_layout(height=400)
                st.plotly_chart(fig_time_score_cat, use_container_width=True)
            
            # Tableau détaillé des modèles de cette catégorie
            st.subheader(f"📊 Tableau Détaillé - Catégorie {selected_category}")
            
            category_summary = category_data.groupby('model').agg({
                'score': ['mean', 'std'],
                'co2 (g)': ['mean', 'sum'],
                'electricity (wh)': ['mean', 'sum'],
                'time (sec)': ['mean', 'std'],
                'tokens': 'mean'
            }).round(2)
            
            # Aplatir les colonnes multi-niveau
            category_summary.columns = ['Score Moyen', 'Score Std', 'CO₂ Moyen', 'CO₂ Total', 
                                      'Élec. Moyenne', 'Élec. Totale', 'Temps Moyen', 'Temps Std', 'Tokens Moyen']
            
            st.dataframe(category_summary, use_container_width=True)
    
    # ===== SECTION 2: COMPARAISON ENTRE CATÉGORIES =====
    with tab2:
        st.header("⚖️ Comparaison entre Catégories de Modèles")
        
        # Analyse comparative des catégories
        category_comparison = filtered_df.groupby('categorie_model').agg({
            'score': ['mean', 'std'],
            'co2 (g)': ['mean', 'sum'],
            'electricity (wh)': ['mean', 'sum'],
            'time (sec)': ['mean', 'std'],
            'tokens': 'mean'
        }).round(2)
        
        # Graphiques de comparaison
        col1, col2 = st.columns(2)
        
        with col1:
            # Comparaison des scores moyens
            score_means = filtered_df.groupby('categorie_model')['score'].mean()
            
            fig_cat_score = px.bar(
                x=score_means.index,
                y=score_means.values,
                title="Score Moyen par Catégorie",
                labels={'x': 'Catégorie', 'y': 'Score moyen'},
                color=score_means.values,
                color_continuous_scale='Viridis'
            )
            fig_cat_score.update_layout(height=400)
            st.plotly_chart(fig_cat_score, use_container_width=True)
            
            # Comparaison des émissions totales
            co2_totals = filtered_df.groupby('categorie_model')['co2 (g)'].sum()
            
            fig_cat_co2 = px.bar(
                x=co2_totals.index,
                y=co2_totals.values,
                title="Émissions CO₂ Totales par Catégorie",
                labels={'x': 'Catégorie', 'y': 'CO₂ total (g)'},
                color=co2_totals.values,
                color_continuous_scale='Reds'
            )
            fig_cat_co2.update_layout(height=400)
            st.plotly_chart(fig_cat_co2, use_container_width=True)
        
        with col2:
            # Boxplot des scores par catégorie
            fig_box_score = px.box(
                filtered_df,
                x='categorie_model',
                y='score',
                title="Distribution des Scores par Catégorie"
            )
            fig_box_score.update_layout(height=400)
            st.plotly_chart(fig_box_score, use_container_width=True)
            
            # Comparaison temps de réponse
            time_means = filtered_df.groupby('categorie_model')['time (sec)'].mean()
            
            fig_cat_time = px.bar(
                x=time_means.index,
                y=time_means.values,
                title="Temps de Réponse Moyen par Catégorie",
                labels={'x': 'Catégorie', 'y': 'Temps moyen (sec)'},
                color=time_means.values,
                color_continuous_scale='Blues'
            )
            fig_cat_time.update_layout(height=400)
            st.plotly_chart(fig_cat_time, use_container_width=True)
        
        # Radar chart pour comparaison multi-critères
        st.subheader("🎯 Comparaison Multi-Critères")
        
        # Normalisation des métriques pour le radar chart
        cat_metrics = filtered_df.groupby('categorie_model').agg({
            'score': 'mean',
            'co2 (g)': 'mean',
            'electricity (wh)': 'mean',
            'time (sec)': 'mean'
        })
        
        # Normaliser (inverser pour CO2, electricity et time car plus bas = mieux)
        cat_metrics_norm = cat_metrics.copy()
        cat_metrics_norm['score'] = cat_metrics_norm['score'] / cat_metrics_norm['score'].max()
        cat_metrics_norm['co2_inv'] = 1 - (cat_metrics_norm['co2 (g)'] / cat_metrics_norm['co2 (g)'].max())
        cat_metrics_norm['elec_inv'] = 1 - (cat_metrics_norm['electricity (wh)'] / cat_metrics_norm['electricity (wh)'].max())
        cat_metrics_norm['time_inv'] = 1 - (cat_metrics_norm['time (sec)'] / cat_metrics_norm['time (sec)'].max())
        
        fig_radar = go.Figure()
        
        for category in cat_metrics_norm.index:
            fig_radar.add_trace(go.Scatterpolar(
                r=[cat_metrics_norm.loc[category, 'score'],
                   cat_metrics_norm.loc[category, 'co2_inv'],
                   cat_metrics_norm.loc[category, 'elec_inv'],
                   cat_metrics_norm.loc[category, 'time_inv']],
                theta=['Performance', 'Efficacité CO₂', 'Efficacité Électrique', 'Rapidité'],
                fill='toself',
                name=category
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Comparaison Radar des Catégories"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Tableau de comparaison
        st.subheader("📊 Tableau Comparatif des Catégories")
        
        category_comparison.columns = ['Score Moyen', 'Score Std', 'CO₂ Moyen', 'CO₂ Total',
                                     'Élec. Moyenne', 'Élec. Totale', 'Temps Moyen', 'Temps Std', 'Tokens Moyen']
        
        st.dataframe(category_comparison, use_container_width=True)
    
    # ===== SECTION 3: COMPARAISON GÉNÉRALE DES MODÈLES =====
    with tab3:
        st.header("🏆 Comparaison Générale des Modèles")
        
        # Calcul de l'efficacité
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['efficacite_co2'] = filtered_df_copy['score'] / (filtered_df_copy['co2 (g)'] + 0.01)
        filtered_df_copy['efficacite_elec'] = filtered_df_copy['score'] / (filtered_df_copy['electricity (wh)'] + 0.01)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top modèles par score
            top_score = filtered_df_copy.groupby('model')['score'].mean().sort_values(ascending=False).head(10)
            
            fig_top_score = px.bar(
                x=top_score.values,
                y=top_score.index,
                orientation='h',
                title="Top 10 - Meilleurs Scores",
                labels={'x': 'Score moyen', 'y': 'Modèle'},
                color=top_score.values,
                color_continuous_scale='Viridis'
            )
            fig_top_score.update_layout(height=500)
            st.plotly_chart(fig_top_score, use_container_width=True)
            
            # Modèles les plus rapides
            fastest_models = filtered_df_copy.groupby('model')['time (sec)'].mean().sort_values(ascending=True).head(10)
            
            fig_fastest = px.bar(
                x=fastest_models.values,
                y=fastest_models.index,
                orientation='h',
                title="Top 10 - Modèles les Plus Rapides",
                labels={'x': 'Temps moyen (sec)', 'y': 'Modèle'},
                color=fastest_models.values,
                color_continuous_scale='Blues_r'
            )
            fig_fastest.update_layout(height=500)
            st.plotly_chart(fig_fastest, use_container_width=True)
        
        with col2:
            # Modèles les plus efficaces (CO2)
            top_efficiency_co2 = filtered_df_copy.groupby('model')['efficacite_co2'].mean().sort_values(ascending=False).head(10)
            
            fig_eff_co2 = px.bar(
                x=top_efficiency_co2.values,
                y=top_efficiency_co2.index,
                orientation='h',
                title="Top 10 - Efficacité CO₂ (Score/g)",
                labels={'x': 'Efficacité CO₂', 'y': 'Modèle'},
                color=top_efficiency_co2.values,
                color_continuous_scale='Greens'
            )
            fig_eff_co2.update_layout(height=500)
            st.plotly_chart(fig_eff_co2, use_container_width=True)
            
            # Modèles avec plus faible empreinte carbone
            lowest_co2 = filtered_df_copy.groupby('model')['co2 (g)'].mean().sort_values(ascending=True).head(10)
            
            fig_low_co2 = px.bar(
                x=lowest_co2.values,
                y=lowest_co2.index,
                orientation='h',
                title="Top 10 - Plus Faible Empreinte Carbone",
                labels={'x': 'CO₂ moyen (g)', 'y': 'Modèle'},
                color=lowest_co2.values,
                color_continuous_scale='Greens'
            )
            fig_low_co2.update_layout(height=500)
            st.plotly_chart(fig_low_co2, use_container_width=True)
        
        # Trade-off global performance vs impact
        st.subheader("🎯 Trade-off Performance vs Impact Environnemental")
        
        plot_data_all = filtered_df_copy.dropna(subset=['score', 'co2 (g)', 'tokens'])
        
        fig_tradeoff_all = px.scatter(
            plot_data_all,
            x='co2 (g)',
            y='score',
            color='categorie_model',
            size='tokens',
            hover_data=['model'],
            title="Performance vs Émissions CO₂ - Tous Modèles",
            labels={'co2 (g)': 'Émissions CO₂ (g)', 'score': 'Score de performance'}
        )
        fig_tradeoff_all.update_layout(height=500)
        st.plotly_chart(fig_tradeoff_all, use_container_width=True)
        
        # Tableau de classement général
        st.subheader("📊 Classement Général des Modèles")
        
        model_ranking = filtered_df_copy.groupby('model').agg({
            'score': 'mean',
            'co2 (g)': 'mean',
            'electricity (wh)': 'mean',
            'time (sec)': 'mean',
            'efficacite_co2': 'mean',
            'tokens': 'mean'
        }).round(2)
        
        # Score global
        model_ranking['score_global'] = (
            (model_ranking['score'] / model_ranking['score'].max()) * 0.4 +
            (model_ranking['efficacite_co2'] / model_ranking['efficacite_co2'].max()) * 0.4 +
            (1 - model_ranking['time (sec)'] / model_ranking['time (sec)'].max()) * 0.2
        ).round(3)
        
        model_ranking = model_ranking.sort_values('score_global', ascending=False)
        model_ranking.columns = ['Score', 'CO₂ (g)', 'Électricité (Wh)', 'Temps (sec)', 'Efficacité CO₂', 'Tokens', 'Score Global']
        
        # Highlighting top 5
        def highlight_top5(row):
            if row.name in model_ranking.index[:5]:
                return ['background-color: #90EE90'] * len(row)
            return [''] * len(row)
        
        styled_ranking = model_ranking.style.apply(highlight_top5, axis=1)
        st.dataframe(styled_ranking, use_container_width=True)
    
    # ===== SECTION 4: ANALYSE PAR TYPE DE QUESTION =====
    with tab4:
        st.header("❓ Analyse par Type de Question")
        
        # Sélection du type de question
        selected_question_type = st.selectbox(
            "Choisissez un type de question à analyser:",
            options=filtered_df['question_categorie'].unique()
        )
        
        question_data = filtered_df[filtered_df['question_categorie'] == selected_question_type]
        
        if not question_data.empty:
            # Métriques pour ce type de question
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Nombre de modèles testés", question_data['model'].nunique())
            with col2:
                st.metric("Score moyen", f"{question_data['score'].mean():.2f}")
            with col3:
                st.metric("Questions de ce type", question_data['question_id'].nunique())
            with col4:
                st.metric("Temps moyen", f"{question_data['time (sec)'].mean():.2f}s")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance par modèle pour ce type de question
                model_perf_q = question_data.groupby('model')['score'].mean().sort_values(ascending=False).head(10)
                
                fig_model_q_score = px.bar(
                    x=model_perf_q.values,
                    y=model_perf_q.index,
                    orientation='h',
                    title=f"Top Modèles - Questions '{selected_question_type}'",
                    labels={'x': 'Score moyen', 'y': 'Modèle'},
                    color=model_perf_q.values,
                    color_continuous_scale='Viridis'
                )
                fig_model_q_score.update_layout(height=400)
                st.plotly_chart(fig_model_q_score, use_container_width=True)
                
                # Distribution des scores pour ce type de question
                fig_dist_q = px.histogram(
                    question_data,
                    x='score',
                    color='categorie_model',
                    title=f"Distribution Scores - Questions '{selected_question_type}'",
                    nbins=10
                )
                fig_dist_q.update_layout(height=400)
                st.plotly_chart(fig_dist_q, use_container_width=True)
            
            with col2:
                # Impact environnemental par catégorie pour ce type de question
                env_by_cat_q = question_data.groupby('categorie_model').agg({
                    'co2 (g)': 'mean',
                    'electricity (wh)': 'mean'
                })
                
                fig_env_q = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('CO₂ Moyen', 'Électricité Moyenne')
                )
                
                fig_env_q.add_trace(
                    go.Bar(x=env_by_cat_q.index, y=env_by_cat_q['co2 (g)'], 
                           name='CO₂', marker_color='lightcoral'),
                    row=1, col=1
                )
                
                fig_env_q.add_trace(
                    go.Bar(x=env_by_cat_q.index, y=env_by_cat_q['electricity (wh)'], 
                           name='Électricité', marker_color='lightblue'),
                    row=1, col=2
                )
                
                fig_env_q.update_layout(height=400, showlegend=False, 
                                      title_text=f"Impact Environnemental - Questions '{selected_question_type}'")
                st.plotly_chart(fig_env_q, use_container_width=True)
                
                # Temps de réponse par catégorie pour ce type de question
                time_by_cat_q = question_data.groupby('categorie_model')['time (sec)'].mean()
                
                fig_time_q = px.bar(
                    x=time_by_cat_q.index,
                    y=time_by_cat_q.values,
                    title=f"Temps de Réponse - Questions '{selected_question_type}'",
                    labels={'x': 'Catégorie', 'y': 'Temps moyen (sec)'},
                    color=time_by_cat_q.values,
                    color_continuous_scale='Blues'
                )
                fig_time_q.update_layout(height=400)
                st.plotly_chart(fig_time_q, use_container_width=True)
            
            # Comparaison des types de questions
            st.subheader("🔄 Comparaison entre Types de Questions")
            
            question_comparison = filtered_df.groupby('question_categorie').agg({
                'score': 'mean',
                'co2 (g)': 'mean',
                'electricity (wh)': 'mean',
                'time (sec)': 'mean',
                'tokens': 'mean'
            }).round(2)
            
            # Graphique comparatif des types de questions
            col1, col2 = st.columns(2)
            
            with col1:
                fig_q_comp_score = px.bar(
                    x=question_comparison.index,
                    y=question_comparison['score'],
                    title="Score Moyen par Type de Question",
                    labels={'x': 'Type de question', 'y': 'Score moyen'},
                    color=question_comparison['score'],
                    color_continuous_scale='Viridis'
                )
                fig_q_comp_score.update_layout(height=400)
                st.plotly_chart(fig_q_comp_score, use_container_width=True)
            
            with col2:
                fig_q_comp_time = px.bar(
                    x=question_comparison.index,
                    y=question_comparison['time (sec)'],
                    title="Temps Moyen par Type de Question",
                    labels={'x': 'Type de question', 'y': 'Temps moyen (sec)'},
                    color=question_comparison['time (sec)'],
                    color_continuous_scale='Reds'
                )
                fig_q_comp_time.update_layout(height=400)
                st.plotly_chart(fig_q_comp_time, use_container_width=True)
            
            # Tableau détaillé pour ce type de question
            st.subheader(f"📊 Tableau Détaillé - Questions '{selected_question_type}'")
            
            question_detail = question_data.groupby(['model', 'categorie_model']).agg({
                'score': ['mean', 'count'],
                'co2 (g)': 'mean',
                'electricity (wh)': 'mean',
                'time (sec)': 'mean'
            }).round(2)
            
            question_detail.columns = ['Score Moyen', 'Nb Questions', 'CO₂ Moyen', 'Élec. Moyenne', 'Temps Moyen']
            
            st.dataframe(question_detail, use_container_width=True)
    
    # Section données brutes (toujours visible)
    st.header("📋 Données Brutes")
    
    if st.checkbox("Afficher les données filtrées"):
        st.dataframe(filtered_df)
        
        # Téléchargement des données filtrées
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données filtrées",
            data=csv,
            file_name="green_ai_filtered_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()