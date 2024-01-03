declare module 'ava' {
	type WatchMode = {
		ignoreChanges: string[];
	};

	type Configuration = {
		files: string[];
		require: string[];
		watchMode: WatchMode;
	};
}
