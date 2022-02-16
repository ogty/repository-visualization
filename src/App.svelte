<script>
	import Folder from './components/Folder.svelte';

	let root = [
		{
			'name': 'settings.py'
		}, 
		{
			'name': 'src', 
			'files': [
				{
					'name': 'README.md'
				}, 
				{
					'name': 'analizer.py'
				}, 
				{
					'name': 'bollinger_band_counter.py'
				}, 
				{
					'name': 'code_acquisition.py'
				}, 
				{
					'name': 'dataframe_slicer.py'
				}, 
				{
					'name': 'download_update.py'
				}, 
				{
					'name': 'historical_volatirity.py'
				}, 
				{
					'name': 'loading.py'
				}, 
				{
					'name': 'market_data_acquisition.py'
				}, 
				{
					'name': 'market_trend.py'
				}, 
				{
					'name': 'schedule_generator.py'
				}, 
				{
					'name': 'stock_data_acquisition.py'
				}, 
				{
					'name': 'text_length_counter.py'
				}, 
				{
					'name': 'totalling.py'
				}
			]
		}, 
		{
			'name': 'README.md'
		}, 
		{
			'name': 'data', 
			'files': [
				{
					'name': 'JP.csv'
				}, 
				{
					'name': 'historical_volatility.png'
				}, 
				{
					'name': 'sample.png'
				}, 
				{
					'name': 'totalling_sample.png'
				}, 
				{
					'name': 'totalling_template.txt'
				}
			]
		}, 
		{
			'name': 'requirements.txt'
		}, 
		{
			'name': '.gitignore'
		}, 
		{
			'name': 'main.py'
		}
	];
</script>

<Folder name="Home" files={root} expanded/>
