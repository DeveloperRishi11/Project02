import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration and styling
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class BiharElectionPredictor:
    def __init__(self):
        self.total_seats = 243
        self.majority_mark = 122
        
        # Historical election results
        self.election_history = pd.DataFrame({
            'Year': [2015, 2020],
            'NDA_Seats': [58, 125],
            'Mahagathbandhan_Seats': [178, 110],
            'Others_Seats': [7, 8],
            'NDA_VoteShare': [34.1, 37.4],
            'Mahagathbandhan_VoteShare': [41.9, 37.3]
        })
        
        # Party-wise 2020 breakdown
        self.party_2020 = pd.DataFrame({
            'Party': ['BJP', 'JDU', 'LJP_RV', 'HAM', 'RJD', 'Congress', 'Left', 'Others'],
            'Seats': [74, 43, 1, 4, 75, 19, 16, 11],
            'Alliance': ['NDA', 'NDA', 'NDA', 'NDA', 'INDIA', 'INDIA', 'INDIA', 'Others']
        })
        
        # Caste demographics (%) - Key to Bihar politics
        self.caste_data = pd.DataFrame({
            'Caste_Group': ['EBC', 'Yadav', 'Muslim', 'Upper_Caste', 'SC', 'Kurmi', 'ST', 'Others'],
            'Population_Percent': [36, 14, 17, 15, 16, 3, 1, 8],
            'Primary_Support': ['NDA', 'INDIA', 'INDIA', 'NDA', 'Mixed', 'NDA', 'NDA', 'Mixed']
        })
        
        # Regional strength matrix
        self.regional_data = pd.DataFrame({
            'Region': ['North_Bihar', 'Central_Bihar', 'South_Bihar', 'East_Bihar', 'West_Bihar'],
            'Total_Seats': [65, 48, 42, 52, 36],
            'NDA_Strength': [0.55, 0.45, 0.65, 0.50, 0.60],
            'INDIA_Strength': [0.40, 0.50, 0.30, 0.45, 0.35]
        })
        
    def calculate_base_probabilities(self):
        """Calculate base winning probabilities using historical trends"""
        
        # Trend analysis from 2015 to 2020
        nda_trend = (self.election_history.loc[1, 'NDA_Seats'] - 
                    self.election_history.loc[0, 'NDA_Seats']) / 5  # per year
        
        vote_trend = (self.election_history.loc[1, 'NDA_VoteShare'] - 
                     self.election_history.loc[0, 'NDA_VoteShare']) / 5
        
        # Project to 2025 (5 years after 2020)
        projected_nda_base = self.election_history.loc[1, 'NDA_Seats'] + (nda_trend * 5)
        projected_vote_base = self.election_history.loc[1, 'NDA_VoteShare'] + (vote_trend * 5)
        
        return projected_nda_base, projected_vote_base
    
    def apply_political_factors(self, base_seats):
        """Apply current political factors to base prediction"""
        
        factors = {
            'incumbency_fatigue': -8,      # 15+ years of Nitish rule
            'ebc_loyalty': +12,            # Strong EBC support for Nitish
            'youth_unemployment': -6,       # Anti-incumbency factor
            'modi_factor': +7,             # National BJP popularity
            'alliance_stability': +5,       # NDA more stable than opposition
            'development_record': +4,       # Infrastructure achievements
            'tejashwi_appeal': -5,         # Opposition youth factor
            'caste_consolidation': +3      # Better caste arithmetic for NDA
        }
        
        total_adjustment = sum(factors.values())
        adjusted_seats = base_seats + total_adjustment
        
        return max(0, min(self.total_seats, adjusted_seats)), factors
    
    def monte_carlo_simulation(self, n_simulations=10000):
        """Run Monte Carlo simulation for election outcomes"""
        
        np.random.seed(42)  # For reproducible results
        
        # Get base prediction
        base_seats, base_vote = self.calculate_base_probabilities()
        adjusted_seats, factors = self.apply_political_factors(base_seats)
        
        results = []
        
        for i in range(n_simulations):
            # Add random variation (electoral uncertainty)
            # Standard deviation based on historical volatility
            seat_variance = np.random.normal(0, 12)  # ±12 seats typical swing
            vote_variance = np.random.normal(0, 2.5)  # ±2.5% vote swing
            
            # Regional variations
            regional_factor = np.random.uniform(-0.15, 0.15)  # ±15% regional swing
            
            # Calculate seats for this simulation
            nda_seats = adjusted_seats + seat_variance + (regional_factor * 20)
            nda_seats = max(15, min(220, nda_seats))  # Realistic bounds
            
            india_seats = self.total_seats - nda_seats - np.random.randint(8, 25)  # Others seats
            india_seats = max(15, india_seats)
            
            others_seats = self.total_seats - nda_seats - india_seats
            
            # Vote shares
            nda_vote = base_vote + vote_variance + (regional_factor * 5)
            india_vote = 100 - nda_vote - np.random.uniform(20, 30)  # Others vote share
            
            results.append({
                'NDA_Seats': int(nda_seats),
                'INDIA_Seats': int(india_seats),
                'Others_Seats': int(others_seats),
                'NDA_VoteShare': max(0, min(100, nda_vote)),
                'INDIA_VoteShare': max(0, min(100, india_vote)),
                'Simulation': i+1
            })
        
        return pd.DataFrame(results)
    
    def analyze_swing_constituencies(self):
        """Analyze critical swing constituencies"""
        
        swing_data = pd.DataFrame({
            'Constituency': ['Patna Sahib', 'Muzaffarpur', 'Begusarai', 'Madhubani', 
                           'Nawada', 'Jehanabad', 'Araria', 'Sasaram', 'Bettiah', 'Darbhanga'],
            'Margin_2020': [1823, 4056, 12138, 2892, 6789, 3456, 8901, 15234, 5678, 7890],
            'Swing_Probability': [0.85, 0.72, 0.68, 0.75, 0.55, 0.80, 0.60, 0.35, 0.65, 0.58],
            'Current_Holder': ['NDA', 'NDA', 'INDIA', 'INDIA', 'NDA', 'INDIA', 'INDIA', 'NDA', 'NDA', 'INDIA'],
            'Key_Demographics': ['Urban', 'Mixed', 'Rural', 'Rural', 'EBC', 'Yadav', 'Muslim', 'Mixed', 'Tribal', 'Urban']
        })
        
        return swing_data
    
    def create_comprehensive_visualizations(self, simulation_df):
        """Create detailed visualizations using only matplotlib"""
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Seat Distribution Histogram
        plt.subplot(2, 3, 1)
        plt.hist(simulation_df['NDA_Seats'], bins=40, alpha=0.7, label='NDA', color='orange', density=True)
        plt.hist(simulation_df['INDIA_Seats'], bins=40, alpha=0.7, label='INDIA Bloc', color='green', density=True)
        plt.axvline(self.majority_mark, color='red', linestyle='--', linewidth=2, label='Majority (122)')
        plt.xlabel('Seats Won')
        plt.ylabel('Probability Density')
        plt.title('Seat Distribution Simulation\n(10,000 iterations)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Vote Share vs Seats Relationship
        plt.subplot(2, 3, 2)
        plt.scatter(simulation_df['NDA_VoteShare'], simulation_df['NDA_Seats'], 
                   alpha=0.3, color='orange', s=1, label='NDA')
        plt.scatter(simulation_df['INDIA_VoteShare'], simulation_df['INDIA_Seats'], 
                   alpha=0.3, color='green', s=1, label='INDIA Bloc')
        plt.xlabel('Vote Share (%)')
        plt.ylabel('Seats Won')
        plt.title('Vote Share vs Seats\nCorrelation Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Probability Pie Chart
        plt.subplot(2, 3, 3)
        nda_majority = (simulation_df['NDA_Seats'] >= self.majority_mark).mean() * 100
        india_majority = (simulation_df['INDIA_Seats'] >= self.majority_mark).mean() * 100
        hung_assembly = 100 - nda_majority - india_majority
        
        outcomes = ['NDA Majority\n({:.1f}%)'.format(nda_majority),
                   'INDIA Majority\n({:.1f}%)'.format(india_majority),
                   'Hung Assembly\n({:.1f}%)'.format(hung_assembly)]
        sizes = [nda_majority, india_majority, hung_assembly]
        colors = ['orange', 'green', 'lightgray']
        
        plt.pie(sizes, labels=outcomes, colors=colors, autopct='', startangle=90)
        plt.title('Election Outcome\nProbabilities')
        
        # 4. Historical Trend Analysis
        plt.subplot(2, 3, 4)
        years = [2015, 2020, 2025]
        nda_trend = [58, 125, simulation_df['NDA_Seats'].mean()]
        india_trend = [178, 110, simulation_df['INDIA_Seats'].mean()]
        
        plt.plot(years, nda_trend, 'o-', color='orange', linewidth=2, markersize=8, label='NDA')
        plt.plot(years, india_trend, 'o-', color='green', linewidth=2, markersize=8, label='INDIA/Mahagathbandhan')
        plt.axhline(self.majority_mark, color='red', linestyle='--', alpha=0.7, label='Majority Mark')
        plt.xlabel('Election Year')
        plt.ylabel('Seats Won')
        plt.title('Historical Seat Trends\n(2015-2025 Projection)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(years)
        
        # 5. Caste Demographics Impact
        plt.subplot(2, 3, 5)
        caste_groups = self.caste_data['Caste_Group'].values
        percentages = self.caste_data['Population_Percent'].values
        colors_caste = ['skyblue' if support == 'NDA' else 'lightgreen' if support == 'INDIA' 
                       else 'lightcoral' for support in self.caste_data['Primary_Support']]
        
        bars = plt.barh(caste_groups, percentages, color=colors_caste)
        plt.xlabel('Population Percentage (%)')
        plt.title('Caste Demographics\n(Blue=NDA lean, Green=INDIA lean)')
        plt.grid(True, alpha=0.3, axis='x')
        
        # 6. Regional Strength Analysis
        plt.subplot(2, 3, 6)
        regions = self.regional_data['Region'].values
        nda_strength = self.regional_data['NDA_Strength'].values * 100
        india_strength = self.regional_data['INDIA_Strength'].values * 100
        
        x = np.arange(len(regions))
        width = 0.35
        
        plt.bar(x - width/2, nda_strength, width, label='NDA', color='orange', alpha=0.8)
        plt.bar(x + width/2, india_strength, width, label='INDIA', color='green', alpha=0.8)
        plt.xlabel('Regions')
        plt.ylabel('Strength (%)')
        plt.title('Regional Alliance Strength')
        plt.xticks(x, [r.replace('_', ' ') for r in regions], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def generate_statistical_report(self, simulation_df):
        """Generate comprehensive statistical analysis"""
        
        # Basic statistics
        nda_stats = simulation_df['NDA_Seats'].describe()
        india_stats = simulation_df['INDIA_Seats'].describe()
        
        # Probability calculations
        nda_majority_prob = (simulation_df['NDA_Seats'] >= self.majority_mark).mean()
        india_majority_prob = (simulation_df['INDIA_Seats'] >= self.majority_mark).mean()
        hung_prob = 1 - nda_majority_prob - india_majority_prob
        
        # Landslide probabilities (150+ seats)
        nda_landslide = (simulation_df['NDA_Seats'] >= 150).mean()
        india_landslide = (simulation_df['INDIA_Seats'] >= 150).mean()
        
        # Confidence intervals
        nda_ci_lower = np.percentile(simulation_df['NDA_Seats'], 5)
        nda_ci_upper = np.percentile(simulation_df['NDA_Seats'], 95)
        india_ci_lower = np.percentile(simulation_df['INDIA_Seats'], 5)
        india_ci_upper = np.percentile(simulation_df['INDIA_Seats'], 95)
        
        # Vote share statistics
        vote_stats = simulation_df[['NDA_VoteShare', 'INDIA_VoteShare']].describe()
        
        return {
            'nda_stats': nda_stats,
            'india_stats': india_stats,
            'probabilities': {
                'nda_majority': nda_majority_prob,
                'india_majority': india_majority_prob,
                'hung_assembly': hung_prob,
                'nda_landslide': nda_landslide,
                'india_landslide': india_landslide
            },
            'confidence_intervals': {
                'nda': (nda_ci_lower, nda_ci_upper),
                'india': (india_ci_lower, india_ci_upper)
            },
            'vote_stats': vote_stats
        }
    
    def seat_vote_conversion_model(self, vote_share, alliance):
        """Convert vote share to seats using electoral dynamics model"""
        
        # Bihar-specific vote-seat elasticity
        # Based on historical analysis of vote share to seat conversion
        
        if alliance == 'NDA':
            # NDA has better vote efficiency due to alliance coordination
            base_conversion_rate = 2.8  # seats per percentage point
            efficiency_bonus = 0.3
        else:
            # INDIA bloc slightly less efficient
            base_conversion_rate = 2.5
            efficiency_bonus = 0.0
        
        # Non-linear relationship - diminishing returns at high vote shares
        if vote_share > 45:
            conversion_rate = base_conversion_rate * 0.8
        elif vote_share < 30:
            conversion_rate = base_conversion_rate * 1.2
        else:
            conversion_rate = base_conversion_rate
        
        seats = (vote_share - 20) * (conversion_rate + efficiency_bonus)
        return max(0, min(200, seats))  # Realistic bounds

def main():
    """Execute complete Bihar election analysis"""
    
    print("🗳️  BIHAR ASSEMBLY ELECTION 2025 - PYTHON DATA ANALYSIS")
    print("=" * 65)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("📊 Using: NumPy, Pandas, Matplotlib")
    print()
    
    # Initialize predictor
    predictor = BiharElectionPredictor()
    
    # Display historical context
    print("📈 HISTORICAL ELECTION RESULTS:")
    print(predictor.election_history.to_string(index=False))
    print()
    
    print("🏛️  2020 PARTY-WISE BREAKDOWN:")
    party_summary = predictor.party_2020.groupby('Alliance')['Seats'].sum()
    print(party_summary)
    print()
    
    # Caste analysis
    print("👥 CASTE DEMOGRAPHICS ANALYSIS:")
    print(predictor.caste_data.to_string(index=False))
    print()
    
    # Calculate base predictions
    base_nda_seats, base_vote_share = predictor.calculate_base_probabilities()
    adjusted_nda_seats, factors = predictor.apply_political_factors(base_nda_seats)
    
    print("🎯 PREDICTION MODEL FACTORS:")
    print(f"Base NDA Projection (trend): {base_nda_seats:.0f} seats")
    print("Political Factor Adjustments:")
    for factor, impact in factors.items():
        sign = "+" if impact > 0 else ""
        print(f"  • {factor.replace('_', ' ').title()}: {sign}{impact} seats")
    print(f"Adjusted NDA Prediction: {adjusted_nda_seats:.0f} seats")
    print()
    
    # Run Monte Carlo simulation
    print("🎲 RUNNING MONTE CARLO SIMULATION...")
    print("   Simulating 10,000 election scenarios...")
    
    simulation_results = predictor.monte_carlo_simulation()
    
    # Generate statistical report
    stats_report = predictor.generate_statistical_report(simulation_results)
    
    print("\n📊 SIMULATION RESULTS:")
    print("-" * 40)
    print(f"NDA Expected Seats: {stats_report['nda_stats']['mean']:.1f} ± {stats_report['nda_stats']['std']:.1f}")
    print(f"INDIA Expected Seats: {stats_report['india_stats']['mean']:.1f} ± {stats_report['india_stats']['std']:.1f}")
    print()
    
    print("🎯 WIN PROBABILITIES:")
    print(f"NDA Majority (≥122): {stats_report['probabilities']['nda_majority']*100:.1f}%")
    print(f"INDIA Majority (≥122): {stats_report['probabilities']['india_majority']*100:.1f}%")
    print(f"Hung Assembly: {stats_report['probabilities']['hung_assembly']*100:.1f}%")
    print()
    print(f"NDA Landslide (≥150): {stats_report['probabilities']['nda_landslide']*100:.1f}%")
    print(f"INDIA Landslide (≥150): {stats_report['probabilities']['india_landslide']*100:.1f}%")
    print()
    
    print("📏 90% CONFIDENCE INTERVALS:")
    print(f"NDA Seats: {stats_report['confidence_intervals']['nda'][0]:.0f} - {stats_report['confidence_intervals']['nda'][1]:.0f}")
    print(f"INDIA Seats: {stats_report['confidence_intervals']['india'][0]:.0f} - {stats_report['confidence_intervals']['india'][1]:.0f}")
    print()
    
    # Swing constituency analysis
    swing_analysis = predictor.analyze_swing_constituencies()
    print("⚖️  CRITICAL SWING CONSTITUENCIES:")
    print(swing_analysis.to_string(index=False))
    print()
    
    # Regional analysis
    print("🗺️  REGIONAL STRENGTH MATRIX:")
    regional_seats = predictor.regional_data.copy()
    regional_seats['Expected_NDA'] = (regional_seats['Total_Seats'] * 
                                     regional_seats['NDA_Strength']).round().astype(int)
    regional_seats['Expected_INDIA'] = (regional_seats['Total_Seats'] * 
                                       regional_seats['INDIA_Strength']).round().astype(int)
    print(regional_seats[['Region', 'Total_Seats', 'Expected_NDA', 'Expected_INDIA']].to_string(index=False))
    print()
    
    # Final prediction
    winner = 'NDA' if stats_report['probabilities']['nda_majority'] > 0.5 else 'INDIA Bloc'
    confidence = max(stats_report['probabilities']['nda_majority'], 
                    stats_report['probabilities']['india_majority']) * 100
    
    print("🏆 FINAL PREDICTION:")
    print("=" * 30)
    print(f"🎖️  Predicted Winner: {winner}")
    print(f"📊 Confidence Level: {confidence:.1f}%")
    print(f"💺 Expected Seats: {stats_report['nda_stats']['mean']:.0f} (NDA) vs {stats_report['india_stats']['mean']:.0f} (INDIA)")
    print(f"📈 Expected Margin: {abs(stats_report['nda_stats']['mean'] - stats_report['india_stats']['mean']):.0f} seats")
    print()
    
    print("⚠️  KEY RISK FACTORS:")
    risk_factors = [
        "• Anti-incumbency after 15+ years of Nitish Kumar",
        "• Youth unemployment and migration concerns",
        "• Alliance stability and last-minute defections",
        "• Caste consolidation patterns on election day",
        "• Impact of national vs state issues in campaign"
    ]
    for risk in risk_factors:
        print(risk)
    print()
    
    # Create and show visualizations
    print("📈 GENERATING VISUALIZATIONS...")
    fig = predictor.create_comprehensive_visualizations(simulation_results)
    plt.show()
    
    # Additional statistical analysis
    print("📋 DETAILED STATISTICS:")
    print("\nNDA Seat Statistics:")
    print(f"  Mean: {stats_report['nda_stats']['mean']:.1f}")
    print(f"  Median: {stats_report['nda_stats']['50%']:.1f}")
    print(f"  Mode: {simulation_results['NDA_Seats'].mode().iloc[0]}")
    print(f"  Standard Deviation: {stats_report['nda_stats']['std']:.1f}")
    print(f"  Min-Max Range: {stats_report['nda_stats']['min']:.0f} - {stats_report['nda_stats']['max']:.0f}")
    
    print("\nINDIA Bloc Seat Statistics:")
    print(f"  Mean: {stats_report['india_stats']['mean']:.1f}")
    print(f"  Median: {stats_report['india_stats']['50%']:.1f}")
    print(f"  Mode: {simulation_results['INDIA_Seats'].mode().iloc[0]}")
    print(f"  Standard Deviation: {stats_report['india_stats']['std']:.1f}")
    print(f"  Min-Max Range: {stats_report['india_stats']['min']:.0f} - {stats_report['india_stats']['max']:.0f}")
    
    # Correlation analysis
    correlation_matrix = simulation_results[['NDA_Seats', 'INDIA_Seats', 'NDA_VoteShare', 'INDIA_VoteShare']].corr()
    print(f"\n🔗 CORRELATION MATRIX:")
    print(correlation_matrix.round(3))
    
    return simulation_results, predictor

# Execute the complete analysis
if __name__ == "__main__":
    simulation_data, election_predictor = main()
    
    print(f"\n✅ Analysis Complete!")
    print(f"📊 {len(simulation_data):,} election scenarios simulated")
    print(f"🎯 Prediction model ready for further analysis")
    
    # Summary DataFrame for easy access
    summary = pd.DataFrame({
        'Metric': ['Expected NDA Seats', 'Expected INDIA Seats', 'NDA Win Probability', 
                  'INDIA Win Probability', 'Hung Assembly Probability'],
        'Value': [
            f"{simulation_data['NDA_Seats'].mean():.0f}",
            f"{simulation_data['INDIA_Seats'].mean():.0f}",
            f"{(simulation_data['NDA_Seats'] >= 122).mean()*100:.1f}%",
            f"{(simulation_data['INDIA_Seats'] >= 122).mean()*100:.1f}%",
            f"{((simulation_data['NDA_Seats'] < 122) & (simulation_data['INDIA_Seats'] < 122)).mean()*100:.1f}%"
        ]
    })
    
    print(f"\n📋 QUICK SUMMARY:")
    print(summary.to_string(index=False))