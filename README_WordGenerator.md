# Advanced Word Generator

A comprehensive word generation system for the SPEED typing application, providing multiple generation strategies with configurable difficulty levels.

## Features

- **Multiple Difficulty Levels**: SIMPLE, MEDIUM, HARD, EXTRA_HARD
- **Various Generation Methods**: Fixed count, session-based, paragraph formatting, mixed difficulties
- **Reproducible Results**: Seed-based random generation for consistent outputs
- **Phrase Support**: Option to preserve multi-word entries as complete units
- **Export Functionality**: Save generated word sets in TSV format
- **Robust Error Handling**: Graceful fallbacks and comprehensive error messages

## Quick Start

```python
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty

# Initialize with optional seed for reproducible results
wg = WordGenerator(seed=7)

# Load default word sources
wg.load_default_sources(allow_phrases=True)

# Generate 50 medium difficulty words
words = wg.generate_words(Difficulty.MEDIUM, count=50)

# Generate words for a 3-minute session at 40 WPM
session_words = wg.generate_for_session(
    Difficulty.MEDIUM, 
    duration_seconds=180, 
    target_wpm=40
)

# Generate paragraph with 6 lines, max 200 characters per line
paragraph = wg.generate_paragraph(
    Difficulty.HARD, 
    lines=6, 
    max_line_chars=200
)

# Generate mixed difficulty words
mixed_words = wg.generate_mixed(
    weights={
        Difficulty.MEDIUM: 0.5,
        Difficulty.HARD: 0.3,
        Difficulty.EXTRA_HARD: 0.2
    },
    total_count=120
)

# Export all words to TSV file
wg.save_merged("merged_words.tsv")
```

## API Reference

### WordGenerator Class

#### Constructor
```python
WordGenerator(seed: Optional[int] = None)
```
- `seed`: Optional seed for reproducible random generation

#### Methods

##### load_default_sources(allow_phrases: bool = False)
Load default word sources for all difficulty levels.
- `allow_phrases`: Whether to preserve multi-word entries as complete units

##### generate_words(difficulty: Difficulty, count: int) -> List[str]
Generate a specific number of words for a given difficulty level.
- `difficulty`: The difficulty level (SIMPLE, MEDIUM, HARD, EXTRA_HARD)
- `count`: The exact number of words to generate
- Returns: List of generated words

##### generate_for_session(difficulty: Difficulty, duration_seconds: int, target_wpm: int) -> List[str]
Generate words for a typing session based on duration and target WPM.
- `difficulty`: The difficulty level
- `duration_seconds`: Session duration in seconds
- `target_wpm`: Target words per minute
- Returns: List of generated words with 10% buffer

##### generate_paragraph(difficulty: Difficulty, lines: int, max_line_chars: int) -> List[str]
Generate words formatted into paragraph lines with character limits.
- `difficulty`: The difficulty level
- `lines`: Number of lines to generate
- `max_line_chars`: Maximum characters per line
- Returns: List of strings, each representing a line

##### generate_mixed(weights: Dict[Difficulty, float], total_count: int) -> List[str]
Generate words with mixed difficulty levels according to specified weights.
- `weights`: Dictionary mapping difficulty levels to their weights (0.0 to 1.0)
- `total_count`: Total number of words to generate
- Returns: List of generated words from mixed difficulties

##### save_merged(filename: str) -> None
Save all available words to a TSV file with difficulty levels.
- `filename`: Path to the output file

##### get_available_difficulties() -> List[Difficulty]
Get list of available difficulty levels.

##### get_word_count_for_difficulty(difficulty: Difficulty) -> int
Get the number of words available for a difficulty level.

##### reload_sources() -> None
Reload all word sources (clears cache).

## Difficulty Levels

### SIMPLE
- Basic, common words (3-6 characters)
- High-frequency vocabulary
- Suitable for beginners

### MEDIUM  
- Intermediate words (5-10 characters)
- Moderate complexity vocabulary
- Balanced challenge level

### HARD
- Advanced words (8-15 characters)
- Complex vocabulary
- Technical and specialized terms

### EXTRA_HARD
- Expert-level words (10+ characters)
- Highly complex vocabulary
- Professional and academic terms

## Configuration

The WordGenerator uses the following default configuration:

```python
{
    'session_buffer_percentage': 10,      # Buffer for session-based generation
    'default_paragraph_lines': 6,         # Default paragraph line count
    'default_line_chars': 200,           # Default max characters per line
    'cache_word_sources': True,          # Enable word source caching
    'export_format': 'tsv'               # Default export format
}
```

## File Structure

```
SPEED/
├── speed_word_generator.py          # Main WordGenerator class
├── models/
│   └── difficulty.py               # Difficulty enum and data models
├── game/
│   └── word_source_loader.py       # Word file loading system
├── simple_words_large.txt          # Simple difficulty words
├── medium_unique_words.txt          # Medium difficulty words
├── hard_words_expanded.txt          # Hard difficulty words
├── extra_hard_words_extended.txt    # Extra hard difficulty words
└── example_usage.py                 # Usage examples
```

## Error Handling

The WordGenerator provides comprehensive error handling:

- **File Loading Errors**: Graceful fallback to available word sources
- **Invalid Parameters**: Clear validation with descriptive error messages
- **Insufficient Words**: Automatic word recycling for large requests
- **Export Errors**: Proper handling of file permissions and disk space issues

## Performance Considerations

- **Caching**: Word sources are cached in memory for fast access
- **Lazy Loading**: Word files are loaded only when needed
- **Efficient Generation**: Optimized algorithms for large word sets
- **Memory Management**: Streaming processing for large requests

## Examples

See `example_usage.py` for comprehensive usage examples that demonstrate all features.

## Testing

The WordGenerator includes extensive unit tests covering:

- Data model validation
- Word source loading
- All generation methods
- Error handling scenarios
- Export functionality
- Performance benchmarks

Run tests with:
```bash
python -m pytest tests/ -v
```

## Integration with SPEED

The WordGenerator integrates seamlessly with the existing SPEED typing application:

- Uses existing word file formats
- Compatible with current database systems
- Extends rather than replaces existing functionality
- Maintains performance standards

## License

Part of the SPEED - Keyboard Speed Training Application.