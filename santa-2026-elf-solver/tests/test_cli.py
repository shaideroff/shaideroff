import csv
import json
from pathlib import Path
from santa_solver.cli import main

def test_cli_inspect_and_validate(tmp_path: Path, capsys):
    puzzles = tmp_path / "puzzles.csv"
    with puzzles.open("w", newline="", encoding="utf-8") as f:
        writer=csv.writer(f); writer.writerow(["id","starting_values","targets","value_limit","registers"])
        writer.writerow(["toy",json.dumps([3]),json.dumps([1,2,5,8]),9,48])
    submission=tmp_path/"submission.csv"
    with submission.open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f); writer.writerow(["id","program"])
        writer.writerow(["toy",json.dumps([["/",0,0,1],["-",0,1,2],["+",0,2,3],["+",0,3,4]])])
    assert main(["inspect",str(puzzles)]) == 0
    assert json.loads(capsys.readouterr().out)["count"] == 1
    assert main(["validate",str(puzzles),str(submission)]) == 0
    output=json.loads(capsys.readouterr().out)
    assert output["total_instructions"] == 4
    assert output["invalid_programs"] == 0

def test_cli_fails_closed_for_malformed_submission(tmp_path: Path, capsys):
    puzzles=tmp_path/"puzzles.csv"
    puzzles.write_text('id,starting_values,targets,value_limit,registers\ntoy,[3],[1],9,48\n',encoding="utf-8")
    submission=tmp_path/"bad.csv"
    submission.write_text('id,program\ntoy,"not json"\n',encoding="utf-8")
    assert main(["validate",str(puzzles),str(submission)]) == 2
    assert "ERROR" in capsys.readouterr().err
