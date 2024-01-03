declare module 'ava' {
    interface IWatchMode {
        ignoreChanges: string[];
    }

    interface IConfig {
        files: string[];
        require: string[];
        watchMode: IWatchMode;
    }
}
