declare module 'ava' {
	type IWatchMode = {
		ignoreChanges: string[];
	};

	type IConfig = {
		files: string[];
		require: string[];
		watchMode: IWatchMode;
	};
}
