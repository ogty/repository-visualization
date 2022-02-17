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

	let root = [{'files': [{'name': 'config.json'},
                                           {'files': [{'name': 'main.css'},
                                                      {'name': 'style.min.css'}],
                                            'name': 'css'},
                                           {'files': [{'name': '32px.png'},
                                                      {'name': 'demo.gif'},
                                                      {'name': 'download_for_linux.png'},
                                                      {'name': 'download_for_mac.png'},
                                                      {'name': 'download_for_windows.png'},
                                                      {'name': 'file_type_pip.png'},
                                                      {'name': 'launch_in_browser.png'},
                                                      {'name': 'throbber.gif'}],
                                            'name': 'images'},
                                           {'files': [{'name': 'jstree.min.js'},
                                                      {'name': 'main.js'}],
                                            'name': 'js'}],
                                 'name': 'static'},
                                {'name': 'requirements.txt'},
                                {'name': 'settings.py'},
                                {'name': 'app.py'},
                                {'name': 'LICENSE'},
                                {'name': '.gitignore'},
                                {'files': [{'name': 'base.py'},
                                           {'name': 'routes.py'}],
                                 'name': 'src'},
                                {'files': [{'name': 'main.py'},
                                           {'name': 'test_install.py'}],
                                 'name': 'test'},
                                {'name': 'README.md'},
                                {'name': 'main.py'},
                                {'files': [{'name': 'main.html'}],
                                 'name': 'templates'}]
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

<Folder name="requirements.txt-generator" files={root} expanded/>
