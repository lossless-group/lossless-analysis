import marimo

__generated_with = "0.13.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    # Path to your CSV file
    file_path = "/Users/mpstaton/code/lossless-monorepo/analysis/private-data/output/2025-05-28_KPIs--Clean--Raw.csv"

    # Read the CSV file with Polars

    df = pl.read_csv(file_path)
    mo.md(f"✅ Successfully loaded: `{file_path}`")
    mo.ui.table(df.head(5))  # Show first 5 rows

    # Return the dataframe for use in other cells
    df
    return df, pl


@app.cell
def _(df, pl):
    # Process data with proper null handling
    df_final = df.sort("month_count").with_columns([
        # Calculate MoM growth with null handling
        pl.when(pl.col("Total Member").is_not_null())
            .then(pl.col("Total Member").pct_change())
            .otherwise(None)
            .alias("mom_growth"),

        # Calculate YoY growth with null handling
        pl.when(pl.col("Total Member").is_not_null())
            .then(pl.col("Total Member").pct_change(12))
            .otherwise(None)
            .alias("yoy_growth")
    ]).with_columns([
        # Format as percentage with null handling
        pl.when(pl.col("mom_growth").is_not_null())
            .then((pl.col("mom_growth") * 100).round(2))
            .otherwise(None)
            .alias("MoM Growth (%)"),

        pl.when(pl.col("yoy_growth").is_not_null())
            .then((pl.col("yoy_growth") * 100).round(2))
            .otherwise(None)
            .alias("YoY Growth (%)")
    ])
    df_final
    return (df_final,)


@app.cell
def _(df_final):
    import plotly.graph_objects as go

    # Hardcode the columns you want to plot
    x_col_label="Timeframe"
    x_col = "month_count"  # Make sure these column names exist in your CSV
    y_col = "Total Member"        # Adjust these to match your actual column names

    # Create the plot
    # Convert Polars Series to Python lists
    x_values = df_final[x_col].to_list()
    y_values = df_final[y_col].to_list()

    # Get unique half_ids and their first occurrence indices
    unique_half_ids = df_final['half_id'].unique().to_list()
    unique_half_ids_list = unique_half_ids
    first_occurrence_indices_list = [df_final['half_id'].to_list().index(half_id) for half_id in unique_half_ids]

    figure1 = go.Figure()
    figure1.add_trace(go.Scatter(
        x=x_values, 
        y=y_values,
        line=dict(color="#af312e"),
        name="Total Members"  # Changed from y_col to the desired display name
        )
    )

    # Update layout
    figure1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        margin=dict(t=150, b=50, l=50, r=50),
        title=f"{y_col} over {x_col_label}",
        xaxis_title=x_col_label,
        yaxis_title=y_col,
        font=dict(family="Helvetica Neue", size=12, color="#2c3e50"),
        title_font=dict(family="Helvetica Neue", size=20, color="#2c3e50"),
        xaxis=dict(
            title_font=dict(family="Helvetica Neue", size=14),
            tickfont=dict(family="Helvetica Neue", size=12),       
            tickmode='array',
            tickvals=first_occurrence_indices_list,
            ticktext=unique_half_ids,
            tickangle=-45, # Optional: angle the labels for better readability
            showticklabels=True
        ),
        yaxis=dict(
            title_font=dict(family="Helvetica Neue", size=14),
            tickfont=dict(family="Helvetica Neue", size=12)
        )
    )

    figure1
    return


if __name__ == "__main__":
    app.run()
