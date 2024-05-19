import sys
import src.interpreter.run as i
import src.transpiler.run as t

class CommandError(Exception):
    pass

def main():
    execute_mode = sys.argv[1]
    # コマンドライン引数の処理
    try:
        if execute_mode == "-i":
            i.run(sys.argv[2:])
        elif execute_mode == "-t":
            t.run(sys.argv[2:])
        else:
            raise CommandError(f"Unknown command: {execute_mode}")
    except CommandError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
  main()
