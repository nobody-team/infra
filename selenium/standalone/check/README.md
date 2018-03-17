## Steps to Check
1. Rename `test.py.template` to `test.py`
2. Run `../entry-shell.sh` with `hub_url` and `target_browsers`, e.g., `http://localhost:4444/wd/hub CHROME,FIREFOX,INTERNETEXPLORER`
3. Following files should be generated
    * `test.py`:  `%hub_url%` replaced with the given parameter
    * `test.py.origin`: the copy of original `test.py`
    * `test_{BROWSER}.py`: the version for BROWSER with `test.py`, e.g., `test_CHROME.py`
    
## Before Docker Build
* Reset `test.py` to its original version in `test.py.origin`
* Clear all generated files
* Uncomment following statements in `../entry-shell.sh`
    ```bash
    #    python ${browser_specific_file}
    #    rm ${browser_specific_file}
    #  mv ${entry}.origin ${entry}
    ```
* Uncomment Dockerfile
    ```
    #ENTRYPOINT ["/workspace/entry-shell.sh", "$hub_url", "$target_browsers"]
    ```
    