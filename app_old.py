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
    
    # ===== SECTION 1: CARTES MÉTRIQUES =====
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
    
    # ===== SECTION 2: COMPARAISON PAR CATÉGORIE =====
    st.header("� Comparaison par Catégorie")
    
    # Analyse par catégorie
    category_analysis = filtered_df.groupby('categorie_model').agg({
        'score': 'mean',
        'time (sec)': 'mean'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # BarChart : Score moyen par catégorie
        fig_score_cat = px.bar(
            x=category_analysis.index,
            y=category_analysis['score'],
            title="Score Moyen par Catégorie",
            labels={'x': 'Catégorie de modèle', 'y': 'Score moyen'},
            color=category_analysis['score'],
            color_continuous_scale='Viridis'
        )
        fig_score_cat.update_layout(height=400)
        st.plotly_chart(fig_score_cat, use_container_width=True)
    
    with col2:
        # BarChart : Temps moyen par catégorie
        fig_time_cat = px.bar(
            x=category_analysis.index,
            y=category_analysis['time (sec)'],
            title="Temps Moyen par Catégorie",
            labels={'x': 'Catégorie de modèle', 'y': 'Temps moyen (sec)'},
            color=category_analysis['time (sec)'],
            color_continuous_scale='Reds'
        )
        fig_time_cat.update_layout(height=400)
        st.plotly_chart(fig_time_cat, use_container_width=True)
    
    # ===== SECTION 3: PERFORMANCE =====
    st.header("⚡ Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temps de Réponse vs Score - ScatterChart
        plot_data_perf = filtered_df.dropna(subset=['time (sec)', 'score'])
        
        fig_time_score = px.scatter(
            plot_data_perf,
            x='time (sec)',
            y='score',
            color='categorie_model',
            size='tokens',
            hover_data=['model'],
            title="Temps de Réponse vs Score",
            labels={'time (sec)': 'Temps de réponse (sec)', 'score': 'Score de performance'}
        )
        fig_time_score.update_layout(height=400)
        st.plotly_chart(fig_time_score, use_container_width=True)
    
    with col2:
        # Nombre de Tokens par Modèle - BarChart horizontal
        tokens_by_model = filtered_df.groupby('model')['tokens'].mean().sort_values(ascending=True)
        
        fig_tokens = px.bar(
            x=tokens_by_model.values,
            y=tokens_by_model.index,
            orientation='h',
            title="Tokens Moyens par Modèle",
            labels={'x': 'Nombre de tokens moyen', 'y': 'Modèle'},
            color=tokens_by_model.values,
            color_continuous_scale='Blues'
        )
        fig_tokens.update_layout(height=400)
        st.plotly_chart(fig_tokens, use_container_width=True)
    
    # ===== SECTION 4: IMPACT ENVIRONNEMENTAL =====
    st.header("🌱 Impact Environnemental")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Impact Environnemental par Catégorie - BarChart
        env_by_category = filtered_df.groupby('categorie_model').agg({
            'electricity (wh)': 'mean',
            'co2 (g)': 'mean'
        }).round(2)
        
        fig_env_cat = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Électricité (Wh)', 'CO₂ (g)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig_env_cat.add_trace(
            go.Bar(x=env_by_category.index, y=env_by_category['electricity (wh)'], 
                   name='Électricité', marker_color='lightblue'),
            row=1, col=1
        )
        
        fig_env_cat.add_trace(
            go.Bar(x=env_by_category.index, y=env_by_category['co2 (g)'], 
                   name='CO₂', marker_color='lightcoral'),
            row=1, col=2
        )
        
        fig_env_cat.update_layout(height=400, showlegend=False, title_text="Impact Environnemental par Catégorie")
        st.plotly_chart(fig_env_cat, use_container_width=True)
    
    with col2:
        # Émissions CO₂ par Modèle - BarChart
        co2_by_model = filtered_df.groupby('model')['co2 (g)'].sum().sort_values(ascending=False)
        
        fig_co2_model = px.bar(
            x=co2_by_model.index,
            y=co2_by_model.values,
            title="Émissions CO₂ Totales par Modèle",
            labels={'x': 'Modèle', 'y': 'CO₂ total (g)'},
            color=co2_by_model.values,
            color_continuous_scale='Reds'
        )
        fig_co2_model.update_layout(height=400)
        fig_co2_model.update_xaxes(tickangle=45)
        st.plotly_chart(fig_co2_model, use_container_width=True)
    
    # ===== SECTION 5: EFFICACITÉ =====
    st.header("� Efficacité")
    
    # Calcul de l'efficacité
    filtered_df = filtered_df.copy()  # Éviter les SettingWithCopyWarning
    filtered_df['efficacite_co2'] = filtered_df['score'] / (filtered_df['co2 (g)'] + 0.01)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Efficacité: Score / CO₂ - BarChart
        efficiency_by_model = filtered_df.groupby('model')['efficacite_co2'].mean().sort_values(ascending=False).head(10)
        
        fig_efficiency = px.bar(
            x=efficiency_by_model.values,
            y=efficiency_by_model.index,
            orientation='h',
            title="Top 10 - Efficacité (Score/CO₂)",
            labels={'x': 'Efficacité (Score/g CO₂)', 'y': 'Modèle'},
            color=efficiency_by_model.values,
            color_continuous_scale='Greens'
        )
        fig_efficiency.update_layout(height=400)
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    with col2:
        # Trade-off: Performance vs Impact - ScatterChart
        plot_data_tradeoff = filtered_df.dropna(subset=['score', 'co2 (g)'])
        
        fig_tradeoff = px.scatter(
            plot_data_tradeoff,
            x='co2 (g)',
            y='score',
            color='categorie_model',
            size='tokens',
            hover_data=['model'],
            title="Trade-off: Performance vs Impact",
            labels={'co2 (g)': 'Émissions CO₂ (g)', 'score': 'Score de performance'}
        )
        fig_tradeoff.update_layout(height=400)
        st.plotly_chart(fig_tradeoff, use_container_width=True)
    
    # Cartes récapitulatives
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏅 Champion d'efficacité")
        best_efficiency = filtered_df.loc[filtered_df['efficacite_co2'].idxmax()]
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write(f"**Modèle:** {best_efficiency['model']}")
        st.write(f"**Efficacité:** {best_efficiency['efficacite_co2']:.2f}")
        st.write(f"**Score:** {best_efficiency['score']}")
        st.write(f"**CO₂:** {best_efficiency['co2 (g)']}g")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("⚠️ Modèle à fort impact")
        worst_co2 = filtered_df.loc[filtered_df['co2 (g)'].idxmax()]
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write(f"**Modèle:** {worst_co2['model']}")
        st.write(f"**CO₂:** {worst_co2['co2 (g)']}g")
        st.write(f"**Score:** {worst_co2['score']}")
        st.write(f"**Électricité:** {worst_co2['electricity (wh)']}Wh")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== SECTION 6: ANALYSE AVANCÉE =====
    st.header("📈 Analyse Avancée")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Qualité vs Consommation Énergétique - ScatterChart
        plot_data_energy = filtered_df.dropna(subset=['score', 'electricity (wh)'])
        
        fig_quality_energy = px.scatter(
            plot_data_energy,
            x='electricity (wh)',
            y='score',
            color='categorie_model',
            size='tokens',
            hover_data=['model'],
            title="Qualité vs Consommation Énergétique",
            labels={'electricity (wh)': 'Consommation électrique (Wh)', 'score': 'Score de qualité'}
        )
        fig_quality_energy.update_layout(height=400)
        st.plotly_chart(fig_quality_energy, use_container_width=True)
    
    with col2:
        # Comparaison de Latence - BarChart horizontal
        latency_by_model = filtered_df.groupby('model')['time (sec)'].mean().sort_values(ascending=True)
        
        fig_latency = px.bar(
            x=latency_by_model.values,
            y=latency_by_model.index,
            orientation='h',
            title="Temps de Réponse par Modèle",
            labels={'x': 'Temps de réponse moyen (sec)', 'y': 'Modèle'},
            color=latency_by_model.values,
            color_continuous_scale='RdYlGn_r'
        )
        fig_latency.update_layout(height=400)
        st.plotly_chart(fig_latency, use_container_width=True)
    
    # Tableau des Meilleurs Compromis
    st.subheader("🎯 Tableau des Meilleurs Compromis")
    
    # Calcul du score global (combinaison de performance et d'efficacité)
    model_summary = filtered_df.groupby('model').agg({
        'score': 'mean',
        'co2 (g)': 'mean',
        'electricity (wh)': 'mean',
        'time (sec)': 'mean',
        'tokens': 'mean',
        'efficacite_co2': 'mean'
    }).round(2)
    
    # Score global normalisé (plus c'est haut, mieux c'est)
    model_summary['score_global'] = (
        (model_summary['score'] / model_summary['score'].max()) * 0.4 +
        (model_summary['efficacite_co2'] / model_summary['efficacite_co2'].max()) * 0.3 +
        (1 - model_summary['time (sec)'] / model_summary['time (sec)'].max()) * 0.3
    ).round(3)
    
    model_summary = model_summary.sort_values('score_global', ascending=False)
    
    # Affichage du tableau avec mise en évidence du top 3
    display_summary = model_summary[['score', 'co2 (g)', 'electricity (wh)', 'time (sec)', 'efficacite_co2', 'score_global']]
    display_summary.columns = ['Score Moyen', 'CO₂ Moyen (g)', 'Électricité (Wh)', 'Temps (sec)', 'Efficacité CO₂', 'Score Global']
    
    # Mise en évidence du top 3
    def highlight_top3(row):
        if row.name in display_summary.index[:3]:
            return ['background-color: #90EE90'] * len(row)
        return [''] * len(row)
    
    styled_summary = display_summary.style.apply(highlight_top3, axis=1)
    st.dataframe(styled_summary, use_container_width=True)
    
    # Top 3 en évidence
    st.subheader("🥇 Top 3 des Meilleurs Compromis")
    col1, col2, col3 = st.columns(3)
    
    top_models = display_summary.index[:3]
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write(f"🥇 **{top_models[0]}**")
        st.write(f"Score Global: {display_summary.loc[top_models[0], 'Score Global']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write(f"🥈 **{top_models[1]}**")
        st.write(f"Score Global: {display_summary.loc[top_models[1], 'Score Global']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write(f"🥉 **{top_models[2]}**")
        st.write(f"Score Global: {display_summary.loc[top_models[2], 'Score Global']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== SECTION 7: DONNÉES BRUTES =====
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