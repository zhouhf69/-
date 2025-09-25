from __future__ import annotations

import argparse
from pathlib import Path

from health_report import AppConfig, Workflow


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="批量生成体检HTML分析报告。")
    parser.add_argument("data_dir", type=Path, help="存放体检原始文件的目录")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("templates/report_template.html"),
        help="HTML模板路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="输出目录",
    )
    parser.add_argument("--hotline", default="400-000-0000", help="24小时热线电话")
    parser.add_argument("--consult", default="400-111-2222", help="健康咨询电话")
    parser.add_argument(
        "--ai-provider",
        default=None,
        help="可选的大模型服务提供商，例如 dashscope (通义千问) 或 zhipu",
    )
    parser.add_argument(
        "--ai-model",
        default=None,
        help="指定模型名称，取决于大模型服务",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = AppConfig.from_args(
        data_dir=args.data_dir,
        template_path=args.template,
        output_dir=args.output,
        hotline=args.hotline,
        consult_line=args.consult,
        ai_provider=args.ai_provider,
        ai_model=args.ai_model,
    )

    workflow = Workflow(config)
    outputs = workflow.run()

    for person_id, path in outputs.items():
        print(f"生成 {person_id} 的报告: {path}")

    if not outputs:
        print("未找到可解析的体检报告文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
