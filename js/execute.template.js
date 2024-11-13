import _ from 'lodash';
import inputs from './inputs.json' assert { type: 'json' };

function test() {
    let originalResults = Array();
    let optimizedResults = Array();
    let refactoredResults = Array();

    let runtimeOriginal = 0;
    {
        // #put ORIGINAL

        let tests1 = JSON.parse(JSON.stringify(inputs.tests));
        let t0 = performance.now();
        tests1.forEach(
            (input) => {
                try {
                    originalResults.push(eval(input))
                }
                catch (e) {
                    originalResults.push(typeof e)
                }
            }
        );
        let t1 = performance.now();
        runtimeOriginal = t1 - t0;

        // Check for exceptions
        let tests2 = JSON.parse(JSON.stringify(inputs.tests));
        let numErrors = 0;
        tests2.forEach(
            (input) => {
                try {
                    eval(input)
                }
                catch (e) {
                    numErrors++;
                }
            }
        );

        if (numErrors === inputs.tests.length)
        {
            console.log(JSON.stringify({
                evaluationError: "Original code does not run properly, all tests return error"
            }));
            return;
        }
    }

    // reset variable name if the name is put in VariableEnvironment through use of var
    try {
        eval(`${inputs.functionName} = null`)
    } catch { }

    let runtimeOptimized = 0;
    {
        // #put OPTIMIZED

        let tests = JSON.parse(JSON.stringify(inputs.tests));
        let t0 = performance.now();
        tests.forEach(
            (input) => {
                try {
                    optimizedResults.push(eval(input))
                }
                catch (e) {
                    optimizedResults.push(typeof e)
                }
            }
        )
        let t1 = performance.now();
        runtimeOptimized = t1 - t0;
    }

    let runtimeRefactored = 0;
    {
        // #put REFACTORED

        let tests = JSON.parse(JSON.stringify(inputs.tests));
        let t0 = performance.now();
        tests.forEach(
            (input) => {
                try {
                    refactoredResults.push(eval(input))
                }
                catch (e) {
                    refactoredResults.push(typeof e)
                }
            }
        )
        let t1 = performance.now();
        runtimeRefactored = t1 - t0;
    }

    if (originalResults.length !== refactoredResults.length)
    {
        console.log(JSON.stringify({
            evaluationError: "Original length != refactored length"
        }));
        return;
    }

    if (originalResults.length !== optimizedResults.length)
    {
        console.log(JSON.stringify({
            evaluationError: "Original length != optimized length"
        }));
        return;
    }

    let numOptimizedCorrect = 0;
    let numRefactoredCorrect = 0;
    originalResults.forEach(
        (exp, i) => {
            if (_.isEqual(exp, refactoredResults[i]))
                numRefactoredCorrect++;

            if (_.isEqual(exp, optimizedResults[i]))
                numOptimizedCorrect++;
        }
    )

    console.log(JSON.stringify({
        runtimeOriginal: runtimeOriginal,
        runtimeOptimized: runtimeOptimized,
        runtimeRefactored: runtimeRefactored,
        numOptimizedCorrect: numOptimizedCorrect,
        numRefactoredCorrect: numRefactoredCorrect,
        total: originalResults.length
    }));
}

try {
    test();
}
catch (e) {
    console.log(JSON.stringify({
        evaluationError: e
    }));
}
