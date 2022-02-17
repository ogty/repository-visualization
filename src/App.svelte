<script>
	import { createForm } from 'felte'
	import { validator } from '@felte/validator-yup'
	import * as yup from 'yup'
	
	import Folder from './components/Folder.svelte';

	const schema = yup.object({
    	username: yup.string().required(),
    	repositoryName: yup.string().required(),
	})

	const { form, errors } = createForm({
		extend: validator,
		validateSchema: schema,
		onSubmit: async (values) => {
			send(JSON.stringify(values, null, 2))
		},
	})

	let username;
	let repositoryName;

	let promise;
	function send(bodyContent) {
		promise = fetch("https://www.google.com/", {
			mode: "cors",
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: bodyContent,
		}).then((x) => x.json());
	};

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

<form use:form on:submit|preventDefault autocomplete="off">
	<input type="text" name="username" placeholder="username" bind:value="{username}"><br>
	<input type="text" name="repositoryName" placeholder="repository" bind:value="{repositoryName}"><br>
	<button type="submit">submit</button>
	{JSON.stringify($errors)}
</form>

{#await promise}
Loading...
{:then data} 
{#if data}
<Folder name="{repositoryName}" files={data} expanded/>
{:else}
nothing
{/if}
{:catch error}
{error}
{/await}

<hr>

<Folder name="HOME" files={root} expanded/>
