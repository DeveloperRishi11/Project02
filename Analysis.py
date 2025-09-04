import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class NDAElectionAnalyzer:
    def __init__(self):
        self.data = {}
        self.colors = {
            'NDA': '#FF6B35',
            'Opposition': '#1A936F', 
            'Neutral': '#88D498'
        }
        
    def generate_approval_data(self):
        """Generate approval rating trends"""
        dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
        
        # Simulate approval ratings with upward trend for NDA
        base_nda = 45
        base_opp = 35
        
        nda_ratings = []
        opp_ratings = []
        
        for i, date in enumerate(dates):
            # Add seasonal and event-based fluctuations
            seasonal = 3 * np.sin(2 * np.pi * i / 12)  # Yearly cycle
            trend = i * 0.3  # Gradual upward trend for NDA
            noise = np.random.normal(0, 2)
            
            nda_score = base_nda + trend + seasonal + noise
            opp_score = base_opp - trend * 0.5 + seasonal * 0.5 + noise
            
            # Ensure realistic bounds
            nda_score = max(30, min(65, nda_score))
            opp_score = max(25, min(50, opp_score))
            
            nda_ratings.append(nda_score)
            opp_ratings.append(opp_score)
        
        self.data['approval'] = pd.DataFrame({
            'Date': dates,
            'NDA': nda_ratings,
            'Opposition': opp_ratings,
            'Undecided': [100 - n - o for n, o in zip(nda_ratings, opp_ratings)]
        })
    
    def generate_performance_metrics(self):
        """Generate government performance metrics"""
        categories = [
            'Economic Growth', 'Infrastructure Development', 'Digital India',
            'Healthcare', 'Foreign Relations', 'Defense & Security',
            'Rural Development', 'Education', 'Clean Energy', 'Employment'
        ]
        
        # Simulate performance scores (higher scores favor NDA)
        nda_scores = [
            72, 78, 85, 68, 82, 88, 70, 65, 80, 62
        ]
        
        opposition_scores = [
            58, 55, 45, 72, 60, 55, 75, 70, 50, 55
        ]
        
        self.data['performance'] = pd.DataFrame({
            'Category': categories,
            'NDA_Score': nda_scores,
            'Opposition_Score': opposition_scores,
            'Advantage': [n - o for n, o in zip(nda_scores, opposition_scores)]
        })
    
    def generate_demographic_support(self):
        """Generate demographic-wise support data"""
        demographics = [
            'Youth (18-35)', 'Middle Age (36-55)', 'Senior (55+)',
            'Urban', 'Rural', 'Business Community',
            'Farmers', 'Women Voters', 'First-time Voters'
        ]
        
        nda_support = [58, 62, 68, 65, 55, 75, 52, 54, 61]
        opposition_support = [35, 32, 28, 30, 40, 20, 43, 41, 32]
        undecided = [7, 6, 4, 5, 5, 5, 5, 5, 7]
        
        self.data['demographics'] = pd.DataFrame({
            'Demographic': demographics,
            'NDA': nda_support,
            'Opposition': opposition_support,
            'Undecided': undecided
        })
    
    def generate_key_achievements(self):
        """Generate key achievement impact scores"""
        achievements = [
            'Digital Payment Revolution',
            'Infrastructure Boom (Roads, Railways)',
            'Direct Benefit Transfer (DBT)',
            'Ayushman Bharat Healthcare',
            'Swachh Bharat Mission',
            'Make in India Initiative',
            'Foreign Policy Successes',
            'Defense Modernization',
            'Renewable Energy Push',
            'Financial Inclusion Programs'
        ]
        
        impact_scores = [88, 85, 82, 78, 80, 72, 86, 84, 79, 81]
        voter_awareness = [92, 88, 85, 82, 95, 70, 75, 68, 65, 78]
        
        self.data['achievements'] = pd.DataFrame({
            'Achievement': achievements,
            'Impact_Score': impact_scores,
            'Voter_Awareness': voter_awareness,
            'Weighted_Score': [i * a / 100 for i, a in zip(impact_scores, voter_awareness)]
        })
    
    def create_approval_trend_chart(self):
        """Create approval rating trend visualization"""
        plt.figure(figsize=(12, 6))
        
        df = self.data['approval']
        plt.plot(df['Date'], df['NDA'], color=self.colors['NDA'], 
                linewidth=3, label='NDA', marker='o', markersize=4)
        plt.plot(df['Date'], df['Opposition'], color=self.colors['Opposition'], 
                linewidth=3, label='Opposition Alliance', marker='s', markersize=4)
        
        plt.fill_between(df['Date'], df['NDA'], alpha=0.3, color=self.colors['NDA'])
        plt.fill_between(df['Date'], df['Opposition'], alpha=0.3, color=self.colors['Opposition'])
        
        plt.title('Approval Rating Trends: Why NDA Leads', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time Period', fontsize=12)
        plt.ylabel('Approval Rating (%)', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Add annotations for latest scores
        latest_nda = df['NDA'].iloc[-1]
        latest_opp = df['Opposition'].iloc[-1]
        plt.annotate(f'NDA: {latest_nda:.1f}%', 
                    xy=(df['Date'].iloc[-1], latest_nda),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=self.colors['NDA'], alpha=0.7),
                    fontweight='bold', color='white')
        
        plt.tight_layout()
        plt.show()
        
        print(f"📈 Current NDA Advantage: {latest_nda - latest_opp:.1f} percentage points")
    
    def create_performance_radar_chart(self):
        """Create performance comparison radar chart"""
        df = self.data['performance']
        
        # Number of variables
        categories = df['Category'].tolist()
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Initialize the spider plot
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot NDA scores
        nda_values = df['NDA_Score'].tolist()
        nda_values += nda_values[:1]
        ax.plot(angles, nda_values, 'o-', linewidth=2, label='NDA', color=self.colors['NDA'])
        ax.fill(angles, nda_values, alpha=0.25, color=self.colors['NDA'])
        
        # Plot Opposition scores
        opp_values = df['Opposition_Score'].tolist()
        opp_values += opp_values[:1]
        ax.plot(angles, opp_values, 'o-', linewidth=2, label='Opposition', color=self.colors['Opposition'])
        ax.fill(angles, opp_values, alpha=0.25, color=self.colors['Opposition'])
        
        # Add category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8)
        ax.grid(True)
        
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        plt.title('Performance Comparison: NDA vs Opposition\n(Higher scores indicate better performance)', 
                 size=14, fontweight='bold', pad=30)
        
        plt.tight_layout()
        plt.show()
        
        # Show advantage summary
        avg_advantage = df['Advantage'].mean()
        winning_categories = len(df[df['Advantage'] > 0])
        print(f"🏆 NDA leads in {winning_categories}/{len(df)} categories")
        print(f"📊 Average performance advantage: {avg_advantage:.1f} points")
    
    def create_demographic_analysis(self):
        """Create demographic support visualization"""
        df = self.data['demographics']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Stacked bar chart
        x = range(len(df))
        width = 0.6
        
        ax1.barh(x, df['NDA'], width, label='NDA', color=self.colors['NDA'], alpha=0.8)
        ax1.barh(x, df['Opposition'], width, left=df['NDA'], 
                label='Opposition', color=self.colors['Opposition'], alpha=0.8)
        ax1.barh(x, df['Undecided'], width, left=df['NDA'] + df['Opposition'],
                label='Undecided', color=self.colors['Neutral'], alpha=0.8)
        
        ax1.set_yticks(x)
        ax1.set_yticklabels(df['Demographic'])
        ax1.set_xlabel('Support Percentage (%)')
        ax1.set_title('Demographic-wise Support Distribution', fontweight='bold')
        ax1.legend()
        ax1.grid(axis='x', alpha=0.3)
        
        # NDA advantage chart
        nda_advantage = df['NDA'] - df['Opposition']
        colors = [self.colors['NDA'] if x > 0 else self.colors['Opposition'] for x in nda_advantage]
        
        ax2.barh(x, nda_advantage, color=colors, alpha=0.7)
        ax2.set_yticks(x)
        ax2.set_yticklabels(df['Demographic'])
        ax2.set_xlabel('NDA Advantage (Percentage Points)')
        ax2.set_title('NDA Lead/Deficit by Demographics', fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Summary statistics
        positive_demos = len(df[df['NDA'] > df['Opposition']])
        avg_lead = (df['NDA'] - df['Opposition']).mean()
        print(f"🎯 NDA leads in {positive_demos}/{len(df)} demographic segments")
        print(f"📈 Average demographic lead: {avg_lead:.1f} percentage points")
    
    def create_achievements_impact(self):
        """Visualize key achievements impact"""
        df = self.data['achievements'].sort_values('Weighted_Score', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        bars = ax.barh(range(len(df)), df['Weighted_Score'], 
                      color=self.colors['NDA'], alpha=0.7)
        
        # Add impact scores as text
        for i, (score, awareness) in enumerate(zip(df['Impact_Score'], df['Voter_Awareness'])):
            ax.text(df['Weighted_Score'].iloc[i] + 1, i, 
                   f'Impact: {score} | Awareness: {awareness}%', 
                   va='center', fontsize=9)
        
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels(df['Achievement'])
        ax.set_xlabel('Weighted Impact Score (Impact × Awareness)', fontsize=12)
        ax.set_title('Key NDA Achievements: Impact on Voter Sentiment', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Show top achievements
        top_3 = df.nlargest(3, 'Weighted_Score')
        print("🏅 Top 3 Most Impactful Achievements:")
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            print(f"  {i}. {row['Achievement']}: {row['Weighted_Score']:.1f} points")
    
    def generate_victory_probability(self):
        """Calculate and display victory probability"""
        # Weighted factors
        factors = {
            'Approval Rating Lead': 25,  # Current lead percentage
            'Performance Advantage': 20,  # Average performance lead
            'Demographic Support': 20,   # Demographics where leading
            'Achievement Impact': 15,    # Weighted achievement scores
            'Historical Advantage': 10,  # Incumbency and past performance
            'Organizational Strength': 10  # Ground-level organization
        }
        
        # Calculate scores
        approval_lead = self.data['approval']['NDA'].iloc[-1] - self.data['approval']['Opposition'].iloc[-1]
        perf_advantage = self.data['performance']['Advantage'].mean()
        demo_lead_count = len(self.data['demographics'][
            self.data['demographics']['NDA'] > self.data['demographics']['Opposition']
        ])
        demo_score = (demo_lead_count / len(self.data['demographics'])) * 100
        achievement_avg = self.data['achievements']['Weighted_Score'].mean()
        
        scores = {
            'Approval Rating Lead': min(100, max(0, approval_lead * 2 + 50)),
            'Performance Advantage': min(100, max(0, perf_advantage * 2 + 50)),
            'Demographic Support': demo_score,
            'Achievement Impact': min(100, achievement_avg),
            'Historical Advantage': 75,  # Assuming strong incumbency
            'Organizational Strength': 80  # Assuming strong organization
        }
        
        # Calculate weighted probability
        total_weighted_score = sum(scores[factor] * weight/100 for factor, weight in factors.items())
        victory_probability = min(95, max(55, total_weighted_score))  # Keep realistic bounds
        
        print("🗳️  NDA ELECTION VICTORY ANALYSIS")
        print("=" * 50)
        print(f"Overall Victory Probability: {victory_probability:.1f}%")
        print("\nDetailed Factor Analysis:")
        
        for factor, weight in factors.items():
            score = scores[factor]
            print(f"  {factor:<25}: {score:5.1f}% (Weight: {weight:2d}%)")
        
        print(f"\nWeighted Average Score: {total_weighted_score:.1f}/100")
        
        # Victory factors summary
        print(f"\n🎯 KEY VICTORY FACTORS:")
        print(f"  • Consistent approval rating lead: {approval_lead:.1f} points")
        print(f"  • Superior performance in {len(self.data['performance'][self.data['performance']['Advantage'] > 0])}/10 key areas")
        print(f"  • Leading in {demo_lead_count}/9 demographic segments")
        print(f"  • Strong achievement track record with high public awareness")
        print(f"  • Organizational advantage and incumbency benefits")
        
        return victory_probability
    
    def run_complete_analysis(self):
        """Run the complete NDA victory analysis"""
        print("🚀 Generating NDA Election Victory Analysis...")
        print("=" * 60)
        
        # Generate all data
        self.generate_approval_data()
        self.generate_performance_metrics()
        self.generate_demographic_support()
        self.generate_key_achievements()
        
        print("📊 Creating Visualizations...\n")
        
        # Create visualizations
        print("1. Approval Rating Trends:")
        self.create_approval_trend_chart()
        print()
        
        print("2. Performance Comparison:")
        self.create_performance_radar_chart()
        print()
        
        print("3. Demographic Analysis:")
        self.create_demographic_analysis()
        print()
        
        print("4. Achievement Impact:")
        self.create_achievements_impact()
        print()
        
        print("5. Victory Probability Calculation:")
        victory_prob = self.generate_victory_probability()
        
        print(f"\n🎊 CONCLUSION: Based on current trends and analysis,")
        print(f"NDA has a {victory_prob:.1f}% probability of electoral victory!")

def main():
    """Main function to run the complete analysis"""
    analyzer = NDAElectionAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()