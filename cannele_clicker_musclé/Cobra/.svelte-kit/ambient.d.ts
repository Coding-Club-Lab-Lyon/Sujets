
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```bash
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const USER: string;
	export const TTY: string;
	export const npm_config_user_agent: string;
	export const npm_node_execpath: string;
	export const SHLVL: string;
	export const LD_LIBRARY_PATH: string;
	export const npm_config_noproxy: string;
	export const HOME: string;
	export const OLDPWD: string;
	export const LESS: string;
	export const NVM_BIN: string;
	export const npm_package_json: string;
	export const ZSH: string;
	export const LSCOLORS: string;
	export const NVM_INC: string;
	export const PAGER: string;
	export const npm_config_userconfig: string;
	export const npm_config_local_prefix: string;
	export const FIG_SET_PARENT_CHECK: string;
	export const CHROME_EXECUTABLE: string;
	export const WSL_DISTRO_NAME: string;
	export const FIG_PID: string;
	export const COLOR: string;
	export const NVM_DIR: string;
	export const npm_config_metrics_registry: string;
	export const WAYLAND_DISPLAY: string;
	export const LOGNAME: string;
	export const NAME: string;
	export const PULSE_SERVER: string;
	export const WSL_INTEROP: string;
	export const _: string;
	export const npm_config_prefix: string;
	export const LC_FIG_SET_PARENT: string;
	export const TERM: string;
	export const npm_config_cache: string;
	export const npm_config_node_gyp: string;
	export const PATH: string;
	export const NODE: string;
	export const npm_package_name: string;
	export const XDG_RUNTIME_DIR: string;
	export const DISPLAY: string;
	export const LANG: string;
	export const FIG_TERM: string;
	export const LS_COLORS: string;
	export const npm_lifecycle_script: string;
	export const SHELL: string;
	export const npm_package_version: string;
	export const npm_lifecycle_event: string;
	export const FIGTERM_SESSION_ID: string;
	export const npm_config_globalconfig: string;
	export const npm_config_init_module: string;
	export const PWD: string;
	export const npm_execpath: string;
	export const FIG_SET_PARENT: string;
	export const NVM_CD_FLAGS: string;
	export const npm_config_global_prefix: string;
	export const npm_command: string;
	export const HOSTTYPE: string;
	export const WSL2_GUI_APPS_ENABLED: string;
	export const WSLENV: string;
	export const INIT_CWD: string;
	export const EDITOR: string;
	export const NODE_ENV: string;
}

/**
 * Similar to [`$env/static/private`](https://kit.svelte.dev/docs/modules#$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/master/packages/adapter-node) (or running [`vite preview`](https://kit.svelte.dev/docs/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env).
 * 
 * This module cannot be imported into client-side code.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		USER: string;
		TTY: string;
		npm_config_user_agent: string;
		npm_node_execpath: string;
		SHLVL: string;
		LD_LIBRARY_PATH: string;
		npm_config_noproxy: string;
		HOME: string;
		OLDPWD: string;
		LESS: string;
		NVM_BIN: string;
		npm_package_json: string;
		ZSH: string;
		LSCOLORS: string;
		NVM_INC: string;
		PAGER: string;
		npm_config_userconfig: string;
		npm_config_local_prefix: string;
		FIG_SET_PARENT_CHECK: string;
		CHROME_EXECUTABLE: string;
		WSL_DISTRO_NAME: string;
		FIG_PID: string;
		COLOR: string;
		NVM_DIR: string;
		npm_config_metrics_registry: string;
		WAYLAND_DISPLAY: string;
		LOGNAME: string;
		NAME: string;
		PULSE_SERVER: string;
		WSL_INTEROP: string;
		_: string;
		npm_config_prefix: string;
		LC_FIG_SET_PARENT: string;
		TERM: string;
		npm_config_cache: string;
		npm_config_node_gyp: string;
		PATH: string;
		NODE: string;
		npm_package_name: string;
		XDG_RUNTIME_DIR: string;
		DISPLAY: string;
		LANG: string;
		FIG_TERM: string;
		LS_COLORS: string;
		npm_lifecycle_script: string;
		SHELL: string;
		npm_package_version: string;
		npm_lifecycle_event: string;
		FIGTERM_SESSION_ID: string;
		npm_config_globalconfig: string;
		npm_config_init_module: string;
		PWD: string;
		npm_execpath: string;
		FIG_SET_PARENT: string;
		NVM_CD_FLAGS: string;
		npm_config_global_prefix: string;
		npm_command: string;
		HOSTTYPE: string;
		WSL2_GUI_APPS_ENABLED: string;
		WSLENV: string;
		INIT_CWD: string;
		EDITOR: string;
		NODE_ENV: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: string]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
